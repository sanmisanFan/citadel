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

    def load_entity_keys(self, entity_keys_file):
        """Load existing entity keys from the JSON file."""
        print(f"DEBUG: Loading entity keys from {entity_keys_file}")
        if os.path.exists(entity_keys_file):
            with open(entity_keys_file, 'r', encoding='utf-8') as f:
                entity_keys = json.load(f)
            print(f"DEBUG: Loaded entity keys: {len(entity_keys.get('authors', {}))} authors, {len(entity_keys.get('venues', {}))} venues")
        else:
            entity_keys = {"authors": {}, "citations": {}, "venues": {}}
            print("DEBUG: No existing entity keys file found, starting with empty keys.")
        return entity_keys

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
            if result is not None:
                return result
            attempts += 1
            print(f"DEBUG: Retry attempt {attempts} for API call with args: {args}")
            sleep(self.request_delay)
        return None

    def _merge_authors(self, s2_authors, openalex_authors=None):
        """
        Merge author lists into the same structure as first-hop enriched data.
        """
        merged_authors = []
        max_length = max(len(s2_authors), len(openalex_authors) if openalex_authors else 0)
        for i in range(max_length):
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
                "raw_name": name  # Default to API name for second hop
            })
        print("DEBUG: Merged authors:", merged_authors)
        return merged_authors

    def _merge_data(self, s2=None, openalex=None):
        """
        Merge Semantic Scholar or OpenAlex data into the same format as first-hop enriched data.
        Prioritizes Semantic Scholar if available, otherwise uses OpenAlex.
        """
        if s2:
            merged = {
                "title": s2.get('title'),
                "authors": self._merge_authors(s2.get('authors', [])),
                "year": s2.get('year'),
                "venue": s2.get('venue'),
                "citation_count": s2.get('citationCount', 0),
                "fields_of_study": s2.get('fieldsOfStudy', []),
                "external_ids": s2.get('externalIds', {}),
                "semantic_scholar_id": s2.get('paperId'),
                "arxiv_id": None,
                "doi": s2.get('externalIds', {}).get('DOI')
            }
        elif openalex:
            merged = {
                "title": openalex.get("title"),
                "authors": self._merge_authors([{"name": a["author"]["display_name"], "externalIds": {"ORCID": a["author"]["orcid"]}} for a in openalex.get("authorships", [])]),
                "year": openalex.get("publication_year"),
                "venue": openalex.get("host_venue", {}).get("display_name"),
                "citation_count": openalex.get("cited_by_count", 0),
                "fields_of_study": [c["display_name"] for c in openalex.get("concepts", [])],
                "external_ids": {"DOI": openalex.get("doi"), "OpenAlex": openalex.get("id")},
                "semantic_scholar_id": None,
                "arxiv_id": None,
                "doi": openalex.get("doi")
            }
        else:
            merged = {}
        print("DEBUG: _merge_data output:", merged)
        return merged

    def assign_entity_keys(self, references_data, entity_keys):
        """
        Assign unique keys for authors, citations, and venues in second-hop references.
        """
        author_key_map = {k: v for k, v in entity_keys["authors"].items()}
        venue_key_map = {v: k for k, v in entity_keys["venues"].items()}
        existing_citation_ids = [int(k.split('-')[1]) for k in entity_keys["citations"].keys() if k.startswith("citation-")]
        citation_counter = max(existing_citation_ids) + 1 if existing_citation_ids else 1
        author_counter = max([int(k.split('-')[1]) for k in entity_keys["authors"].keys()] + [0]) + 1
        venue_counter = max([int(k.split('-')[1]) for k in entity_keys["venues"].keys()] + [0]) + 1

        for paper_id, data in references_data.items():
            enriched_refs = data["references"]
            for ref in enriched_refs:
                # Process authors
                new_authors = []
                for author in ref.get("authors", []):
                    author_name = author.get("name", "").strip()
                    orcid = author.get("orcid")
                    key_tuple = (author_name.lower(), orcid)
                    if key_tuple in author_key_map:
                        a_key = author_key_map[key_tuple]["key"]
                    else:
                        a_key = f"author-{author_counter}"
                        author["key"] = a_key
                        author_key_map[key_tuple] = author
                        entity_keys["authors"][a_key] = author
                        author_counter += 1
                    new_authors.append(a_key)
                ref["authors"] = new_authors

                # Process venue
                venue = ref.get("venue")
                if venue:
                    venue_str = str(venue)
                    if venue_str in venue_key_map:
                        v_key = venue_key_map[venue_str]
                    else:
                        v_key = f"venue-{venue_counter}"
                        venue_key_map[venue_str] = v_key
                        entity_keys["venues"][v_key] = venue_str
                        venue_counter += 1
                    ref["venue"] = v_key

                # Assign citation key
                citation_key = f"citation-{citation_counter}"
                citation_counter += 1
                ref["citation_key"] = citation_key
                entity_keys["citations"][citation_key] = {
                    "title": ref["title"],
                    "authors": ref["authors"],
                    "venue": ref["venue"],
                    "year": ref["year"],
                    "citation_count": ref.get("citation_count", 0),
                    "fields_of_study": ref.get("fields_of_study", []),
                    "external_ids": ref.get("external_ids", {}),
                    "semantic_scholar_id": ref["semantic_scholar_id"],
                    "arxiv_id": ref.get("arxiv_id"),
                    "doi": ref["doi"],
                    "second_hop": "yes"
                }

        return references_data, entity_keys

    def process_second_hop(self, input_file, output_file, entity_keys_file):
        """
        Process second-hop references, falling back to OpenAlex if Semantic Scholar fails.
        """
        papers = self.load_enriched_papers(input_file)
        entity_keys = self.load_entity_keys(entity_keys_file)
        all_references = {}

        for idx, paper in enumerate(papers, 1):
            paper_id = paper.get("semantic_scholar_id")
            title = paper.get("title")
            if not paper_id:
                print(f"DEBUG: Paper {idx} with title '{title}' has no semantic_scholar_id. Skipping second hop.")
                continue
            print(f"DEBUG: Processing second hop for paper {idx} with title: {title} (ID: {paper_id})")

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
                if details is None:
                    print(f"DEBUG: Semantic Scholar failed for {ref_paper_id}, falling back to OpenAlex with title: {ref.get('title')}")
                    openalex_data = self.retry_api_call(self.get_paper_details_openalex, ref.get("title"))
                    if openalex_data:
                        merged = self._merge_data(openalex=openalex_data)
                    else:
                        print(f"DEBUG: OpenAlex also failed for title {ref.get('title')}, skipping reference")
                        continue
                else:
                    openalex_authors = None
                    need_openalex_supplement = False
                    if "authors" in details:
                        for author in details.get("authors", []):
                            orcid = (author.get('externalIds') or {}).get('ORCID')
                            if not orcid:
                                need_openalex_supplement = True
                                break
                    else:
                        need_openalex_supplement = True
                    if need_openalex_supplement:
                        print("DEBUG: ORCID missing, supplementing with OpenAlex data")
                        openalex_data = self.retry_api_call(self.get_paper_details_openalex, details.get("title"))
                        if openalex_data:
                            openalex_authors = [{"name": a["author"]["display_name"], "orcid": a["author"]["orcid"]} for a in openalex_data.get("authorships", [])]
                    merged = self._merge_data(s2=details, openalex=openalex_authors)
                
                enriched_refs.append(merged)
                sleep(self.request_delay)

            all_references[paper_id] = {
                "title": title,
                "references": enriched_refs
            }

        # Assign entity keys to second-hop references
        all_references, entity_keys = self.assign_entity_keys(all_references, entity_keys)

        # Save results
        print(f"DEBUG: Saving second hop references to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_references, f, indent=2, ensure_ascii=False)
        print(f"DEBUG: Saving updated entity keys to {entity_keys_file}")
        with open(entity_keys_file, 'w', encoding='utf-8') as f:
            json.dump(entity_keys, f, indent=2, ensure_ascii=False)
        print("DEBUG: Second hop processing complete.")

if __name__ == "__main__":
    processor = SecondHopProcessor()
    processor.process_second_hop(
        "outputs/enriched_papers.json",
        "outputs/second_hop_references.json",
        "outputs/entity_keys.json"
    )