import requests
import json
from time import sleep
import os

class SecondHopProcessor:
    def __init__(self):
        self.s2_base = "https://api.semanticscholar.org/graph/v1"
        self.max_retries = 3
        self.request_delay = 1
        print("DEBUG: Initialized SecondHopProcessor with Semantic Scholar base URL:", self.s2_base)
    
    def load_enriched_papers(self, input_file):
        """Load first-hop enriched papers from JSON file."""
        print(f"DEBUG: Loading enriched papers from {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        print(f"DEBUG: Loaded {len(papers)} enriched papers")
        return papers

    def get_references_for_paper(self, paper_id):
        """
        Fetches the references (papers cited) for a given paper using Semantic Scholar.
        Requests basic fields for each reference.
        If a 429 (Too Many Requests) response is received, sleeps for 30 seconds before returning.
        """
        fields = "references.paperId,references.title,references.authors,references.venue,references.year"
        url = f"{self.s2_base}/paper/{paper_id}"
        params = {"fields": fields}
        print(f"DEBUG: Fetching references for paper ID: {paper_id}")
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 429:
                print(f"DEBUG: Received 429 Too Many Requests for paper ID: {paper_id}. Sleeping for 30 seconds.")
                sleep(30)
                return None
            response.raise_for_status()
            data = response.json()
            refs = data.get("references", [])
            print(f"DEBUG: Found {len(refs)} references for paper ID: {paper_id}")
            return refs
        except Exception as e:
            print(f"DEBUG: Error fetching references for paper ID {paper_id}: {e}")
            return None

    def get_paper_details(self, paper_id):
        """
        Fetch full details for a paper from Semantic Scholar.
        The returned data includes title, authors (with authorId and externalIds), venue,
        year, citationCount, fieldsOfStudy, externalIds, and paperId.
        """
        fields = (
            "title,authors.name,authors.authorId,authors.externalIds,"
            "venue,year,citationCount,fieldsOfStudy,externalIds,paperId"
        )
        url = f"{self.s2_base}/paper/{paper_id}"
        params = {"fields": fields}
        print(f"DEBUG: Fetching full details for paper ID: {paper_id}")
        try:
            response = requests.get(url, params=params, timeout=15)
            print("DEBUG: get_paper_details response status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            print("DEBUG: Received details for paper ID:", paper_id, data)
            return data
        except Exception as e:
            print(f"DEBUG: Error fetching details for paper ID {paper_id}: {e}")
            return None

    def get_paper_details_openalex(self, title):
        """Fetch paper details from OpenAlex by title."""
        openalex_url = "https://api.openalex.org/works"
        params = {
            "filter": f"title.search:{title}",
            "per-page": 1  # Only get the top result
        }
        print(f"DEBUG: Fetching OpenAlex details for title: {title}")
        try:
            response = requests.get(openalex_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                print("DEBUG: Received OpenAlex data:", data["results"][0])
                return data["results"][0]
            else:
                print("DEBUG: No results found on OpenAlex for title:", title)
                return None
        except Exception as e:
            print(f"DEBUG: OpenAlex API request failed for title {title}: {e}")
            return None

    def retry_api_call(self, func, *args):
        """Generic retry mechanism for API calls."""
        attempts = 0
        while attempts < self.max_retries:
            result = func(*args)
            # We treat an empty list as a valid result, but None indicates failure.
            if result is not None:
                return result
            attempts += 1
            print(f"DEBUG: Retry attempt {attempts} for API call with args: {args}")
            sleep(self.request_delay)
        return None

    def _merge_authors(self, parsed_authors, s2_authors, openalex_authors=None):
        """
        Merge author lists so that each author object has the same structure as your
        first-hop enriched data. For each author from Semantic Scholar, include:
          - name
          - s2_id (from authorId)
          - orcid (from externalIds if available, or fallback to OpenAlex)
          - raw_name (fallback from the parsed authors list if available)
        """
        merged_authors = []
        max_length = max(len(parsed_authors), len(s2_authors))
        for i in range(max_length):
            raw_name = parsed_authors[i] if i < len(parsed_authors) else None
            if i < len(s2_authors) and s2_authors[i]:
                api_author = s2_authors[i]
            elif openalex_authors and i < len(openalex_authors):
                api_author = openalex_authors[i]
            else:
                api_author = {}
            name = api_author.get('name')
            s2_id = api_author.get('authorId')
            orcid = None
            if api_author:
                ext_ids = api_author.get('externalIds') or {}
                orcid = ext_ids.get('ORCID')
            if not orcid and openalex_authors and i < len(openalex_authors):
                orcid = openalex_authors[i].get("orcid")
            merged_authors.append({
                "name": name,
                "s2_id": s2_id,
                "orcid": orcid,
                "raw_name": raw_name
            })
        print("DEBUG: Merged authors:", merged_authors)
        return merged_authors

    def _merge_data(self, parsed, s2, openalex_authors=None):
        """
        Merge the parsed data (from first hop or minimal reference data) with Semantic Scholar
        details (from second hop) so that the result is in the same format as your first-hop enriched data.
        """
        merged = {
            "title": s2.get('title', parsed.get('title')),
            "authors": self._merge_authors(parsed.get('authors', []), s2.get('authors', []), openalex_authors),
            "year": s2.get('year', parsed.get('year')),
            "venue": s2.get('venue', parsed.get('venue')),
            "citation_count": s2.get('citationCount', 0),
            "fields_of_study": s2.get('fieldsOfStudy', []),
            "external_ids": s2.get('externalIds', {}),
            "semantic_scholar_id": s2.get('paperId'),
            "arxiv_id": parsed.get('arxiv_id'),
            "doi": s2.get('externalIds', {}).get('DOI', parsed.get('doi'))
        }
        print("DEBUG: _merge_data output:", merged)
        return merged

    def process_second_hop(self, input_file, output_file):
        """
        For each enriched paper (first hop) in the input JSON file, fetch its references.
        For each reference, retrieve full details (including authors, DOI, etc.) and
        merge the data in the same format as your first hop.
        The complete second hop data is saved to the output JSON file.
        """
        papers = self.load_enriched_papers(input_file)
        all_references = {}
        for idx, paper in enumerate(papers, 1):
            paper_id = paper.get("semantic_scholar_id")
            title = paper.get("title")
            if not paper_id:
                print(f"DEBUG: Paper {idx} with title '{title}' has no semantic_scholar_id. Skipping second hop.")
                continue
            print(f"DEBUG: Processing second hop for paper {idx} with title: {title} (ID: {paper_id})")
            
            # Use retry mechanism for fetching references.
            refs = self.retry_api_call(self.get_references_for_paper, paper_id)
            if refs is None:
                print(f"DEBUG: Skipping paper {paper_id} due to failure in fetching references.")
                continue

            enriched_refs = []
            for ref in refs:
                ref_paper_id = ref.get("paperId")
                if not ref_paper_id:
                    print("DEBUG: Reference without paperId, skipping")
                    continue
                print(f"DEBUG: Enriching reference with paperId: {ref_paper_id}")
                details = self.retry_api_call(self.get_paper_details, ref_paper_id)
                openalex_authors = None
                if details:
                    need_openalex = False
                    if "authors" in details:
                        for author in details.get("authors", []):
                            orcid = (author.get('externalIds') or {}).get('ORCID')
                            if not orcid:
                                need_openalex = True
                                break
                    else:
                        need_openalex = True
                    if need_openalex:
                        print("DEBUG: ORCID missing for reference, attempting fallback via OpenAlex")
                        openalex_data = self.get_paper_details_openalex(details.get("title"))
                        if openalex_data:
                            openalex_authors = []
                            for authorship in openalex_data.get("authorships", []):
                                openalex_authors.append({
                                    "name": authorship.get("author", {}).get("display_name"),
                                    "orcid": authorship.get("author", {}).get("orcid")
                                })
                    # For second hop references, we use minimal parsed data (empty authors list)
                    merged = self._merge_data({"authors": []}, details, openalex_authors)
                    enriched_refs.append(merged)
                    sleep(self.request_delay)
            all_references[paper_id] = {
                "title": title,
                "references": enriched_refs
            }
        print(f"DEBUG: Saving second hop references to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_references, f, indent=2, ensure_ascii=False)
        print("DEBUG: Second hop processing complete.")

if __name__ == "__main__":
    processor = SecondHopProcessor()
    # Replace "enriched_papers.json" with your first-hop file if different.
    processor.process_second_hop("enriched_papers.json", "second_hop_references.json")
