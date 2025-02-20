import requests
import json
from time import sleep
import os
from openai import OpenAI

class PaperProcessor:
    def __init__(self):
        self.s2_base = "https://api.semanticscholar.org/graph/v1"
        self.max_retries = 3
        self.request_delay = 1
        self.gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("DEBUG: Initialized PaperProcessor with Semantic Scholar base URL:", self.s2_base)
        
    def parse_reference_with_gpt(self, ref_text):
        """
        Use GPT to extract structured data from reference text.
        If the reference contains 'et al.', only include the explicitly mentioned author(s).
        In addition, if the venue appears abbreviated, expand it to its full name and store it in "venue",
        while saving the originally mentioned venue in "raw_venue".
        """
        prompt = f"""
Parse this academic reference into JSON format with the following keys: authors (array), title, venue, raw_venue, year, pages, arxiv_id, and doi.
If the venue name in the reference appears abbreviated, expand it to its full name and save the expanded version in "venue",
while preserving the original text in "raw_venue". Handle incomplete information using null for missing fields.

Reference: "{ref_text}"

Return JSON only, no commentary.
Example:
{{
  "authors": ["Author 1", "Author 2"],
  "title": "Paper Title",
  "venue": "International Conference on Very Large Data Bases",
  "raw_venue": "VLDB",
  "year": 2023,
  "pages": "123-145",
  "arxiv_id": "1234.5678",
  "doi": "10.1234/abcd"
}}
"""
        print("DEBUG: Sending GPT prompt for reference:", ref_text)
        try:
            response = self.gpt_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            gpt_output = response.choices[0].message.content
            print("DEBUG: Received GPT response:", gpt_output)
            result = json.loads(gpt_output)
            # Filter out any "et al" entries from the GPT authors array
            if "authors" in result:
                result["authors"] = [author for author in result["authors"] if "et al" not in author.lower()]
            return result
        except Exception as e:
            print(f"DEBUG: GPT parsing failed for reference: {ref_text} with error: {e}")
            return None

    def load_and_parse_input(self, input_file):
        """Process text file into structured papers.
           Also, assign a reference id (ref_id) to each paper for later merging."""
        print(f"DEBUG: Loading input file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            references = [line.strip() for line in f if line.strip()]
        
        print(f"DEBUG: Found {len(references)} references in the input file")
        parsed_papers = []
        for idx, ref in enumerate(references, 1):
            print(f"DEBUG: Parsing reference {idx}: {ref}")
            paper_data = self.parse_reference_with_gpt(ref)
            if paper_data:
                print(f"DEBUG: Successfully parsed reference {idx}")
                # Add a reference identifier for later use
                paper_data["ref_id"] = idx
                parsed_papers.append(paper_data)
                sleep(1)  # Rate limit GPT requests
            else:
                print(f"DEBUG: Failed to parse reference {idx}: {ref}")
        return parsed_papers

    def load_reference_mentions(self, ref_file):
        """Load reference mentions from a JSON file and return a mapping from reference id to texts."""
        print("DEBUG: Loading reference mentions file:", ref_file)
        with open(ref_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        mapping = {}
        for item in data:
            ref_number = item.get("reference")
            if ref_number is not None:
                mapping[ref_number] = item.get("texts", [])
        return mapping

    def get_paper_details(self, paper_id):
        """Fetch complete paper details from Semantic Scholar using the paper ID"""
        fields = (
            "title,authors.name,authors.authorId,authors.externalIds,"
            "venue,year,citationCount,fieldsOfStudy,externalIds,paperId"
        )
        print(f"DEBUG: Fetching Semantic Scholar details for paper ID: {paper_id}")
        try:
            response = requests.get(
                f"{self.s2_base}/paper/{paper_id}",
                params={"fields": fields},
                timeout=15
            )
            print("DEBUG: Semantic Scholar API response status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            print("DEBUG: Received Semantic Scholar data:", data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: API request failed for paper ID {paper_id}: {e}")
            return None

    def get_paper_details_openalex(self, title):
        """Fetch paper details from OpenAlex by title"""
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

    def enrich_paper_data(self, parsed_data):
        """Enrich GPT-parsed data by always searching Semantic Scholar by title,
           and if ORCID data is missing, fall back to OpenAlex."""
        print("DEBUG: Starting enrichment of GPT parsed data")
        enriched = []
        for i, paper in enumerate(parsed_data, 1):
            title = paper.get('title')
            if not title:
                print(f"DEBUG: Paper {i} has no title. Skipping Semantic Scholar search.")
                continue

            print(f"DEBUG: Searching Semantic Scholar for paper {i} with title: {title}")
            paper_id = self.search_paper(title)
            s2_data = None
            if paper_id:
                print(f"DEBUG: Found paper ID {paper_id} for paper {i}")
                s2_data = self.retry_api_call(self.get_paper_details, paper_id)
            else:
                print(f"DEBUG: No paper found in Semantic Scholar for paper {i} with title: {title}")

            need_openalex = False
            # Check if Semantic Scholar returned data and if any author is missing ORCID.
            if s2_data and "authors" in s2_data:
                for author in s2_data.get("authors", []):
                    orcid = (author.get('externalIds') or {}).get('ORCID')
                    if not orcid:
                        need_openalex = True
                        break
            else:
                need_openalex = True

            openalex_data = None
            openalex_authors = None
            if need_openalex:
                print(f"DEBUG: ORCID missing or Semantic Scholar data not available for paper {i}, attempting fallback via OpenAlex")
                openalex_data = self.get_paper_details_openalex(title)
                if openalex_data:
                    # OpenAlex returns authors under 'authorships'
                    openalex_authors = []
                    for authorship in openalex_data.get("authorships", []):
                        openalex_authors.append({
                            "name": authorship.get("author", {}).get("display_name"),
                            "orcid": authorship.get("author", {}).get("orcid")
                        })

            if s2_data:
                merged = self._merge_data(paper, s2_data, openalex_authors)
                print(f"DEBUG: Merged data for paper {i}: {merged}")
                enriched.append(merged)
            elif openalex_data:
                # Fallback: merge using OpenAlex data if Semantic Scholar data is not available.
                merged = self._merge_data_openalex(paper, openalex_data)
                print(f"DEBUG: Merged OpenAlex data for paper {i}: {merged}")
                enriched.append(merged)
            else:
                print(f"DEBUG: No data found for paper {i} on both Semantic Scholar and OpenAlex")
            sleep(self.request_delay)
        return enriched

    def _merge_data(self, parsed, s2, openalex_authors=None):
        """
        Combine GPT parsing with Semantic Scholar data, using OpenAlex fallback for authors if needed.
        For venue, use the GPT-expanded full conference name from parsed["venue"] and preserve the original
        as parsed["raw_venue"].
        """
        venue_full = parsed.get('venue') if 'venue' in parsed else s2.get('venue')
        raw_venue = parsed.get('raw_venue') if 'raw_venue' in parsed else s2.get('venue', parsed.get('venue'))
        merged = {
            "title": s2.get('title', parsed.get('title')),
            "authors": self._merge_authors(parsed.get('authors', []), s2.get('authors', []), openalex_authors),
            "year": s2.get('year', parsed.get('year')),
            "venue": venue_full,       # GPT-expanded full conference name
            "raw_venue": raw_venue,      # Venue as mentioned in the reference
            "citation_count": s2.get('citationCount', 0),
            "fields_of_study": s2.get('fieldsOfStudy', []),
            "external_ids": s2.get('externalIds', {}),
            "semantic_scholar_id": s2.get('paperId'),
            "arxiv_id": parsed.get('arxiv_id'),
            "doi": s2.get('externalIds', {}).get('DOI', parsed.get('doi'))
        }
        if "ref_id" in parsed:
            merged["ref_id"] = parsed["ref_id"]
        print("DEBUG: _merge_data output:", merged)
        return merged

    def _merge_data_openalex(self, parsed, openalex):
        """
        Merge data using OpenAlex response when Semantic Scholar data is not available.
        For venue, use the GPT-expanded full conference name from parsed["venue"] and preserve the original
        as parsed["raw_venue"].
        """
        title = openalex.get("display_name", parsed.get("title"))
        openalex_authors = []
        for authorship in openalex.get("authorships", []):
            openalex_authors.append({
                "name": authorship.get("author", {}).get("display_name"),
                "orcid": authorship.get("author", {}).get("orcid")
            })
        venue_full = parsed.get('venue') if 'venue' in parsed else openalex.get("host_venue", {}).get("display_name")
        raw_venue = parsed.get('raw_venue') if 'raw_venue' in parsed else openalex.get("host_venue", {}).get("display_name", parsed.get("venue"))
        merged = {
            "title": title,
            "authors": openalex_authors,
            "year": openalex.get("publication_year", parsed.get("year")),
            "venue": venue_full,       # GPT-expanded full venue
            "raw_venue": raw_venue,      # Original venue from reference
            "citation_count": openalex.get("citation_count", 0),
            "fields_of_study": openalex.get("concepts", []),
            "external_ids": {"OpenAlex": openalex.get("id")},
            "semantic_scholar_id": None,
            "arxiv_id": parsed.get('arxiv_id'),
            "doi": openalex.get("doi", parsed.get("doi"))
        }
        if "ref_id" in parsed:
            merged["ref_id"] = parsed["ref_id"]
        print("DEBUG: _merge_data_openalex output:", merged)
        return merged

    def _merge_authors(self, parsed_authors, s2_authors, openalex_authors=None):
        """
        Combine author lists ensuring:
         - The raw_name comes from the GPT (parsed reference) output.
         - The normalized name (and other metadata) comes from the API response.
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

    def assign_entity_keys(self, enriched):
        """
        Assign unique keys for each author, citation, and venue.
        Each unique author gets a key "author-<number>", each enriched paper gets a citation key "citation-<number>",
        and each unique venue gets a key "venue-<number>".
        The keys and associated details are stored in a dictionary that will be written to a separate JSON file.
        Note: The unique venue key is generated based solely on the API venue (i.e. the GPT-expanded full venue).
        """
        entity_keys = {"authors": {}, "citations": {}, "venues": {}}
        author_key_map = {}
        venue_key_map = {}
        citation_counter = 1
        author_counter = 1
        venue_counter = 1

        for paper in enriched:
            citation_key = f"citation-{citation_counter}"
            citation_counter += 1
            paper["citation_key"] = citation_key
            entity_keys["citations"][citation_key] = paper

            new_authors = []
            for author in paper.get("authors", []):
                if isinstance(author, str):
                    new_authors.append(author)
                    continue
                author_name = author.get("name", "").strip()
                orcid = author.get("orcid")
                key_tuple = (author_name.lower(), orcid)
                if key_tuple not in author_key_map:
                    a_key = f"author-{author_counter}"
                    author_counter += 1
                    author_key_map[key_tuple] = a_key
                    entity_keys["authors"][a_key] = author
                else:
                    a_key = author_key_map[key_tuple]
                new_authors.append(a_key)
            paper["authors"] = new_authors

            venue = paper.get("venue")
            if venue:
                venue_str = venue if isinstance(venue, str) else str(venue)
                if venue_str not in venue_key_map:
                    v_key = f"venue-{venue_counter}"
                    venue_counter += 1
                    venue_key_map[venue_str] = v_key
                    entity_keys["venues"][v_key] = venue_str
                else:
                    v_key = venue_key_map[venue_str]
                paper["venue"] = v_key
        return enriched, entity_keys

    def process_papers(self, input_file, output_file, reference_mentions_file=None):
        """End-to-end processing pipeline. Optionally merges reference mention data if a JSON file is provided."""
        print("DEBUG: Starting processing of papers")
        print("DEBUG: Parsing input file with GPT...")
        parsed = self.load_and_parse_input(input_file)
        
        ref_mentions = {}
        if reference_mentions_file:
            ref_mentions = self.load_reference_mentions(reference_mentions_file)
        
        print("DEBUG: Enriching with Semantic Scholar (and OpenAlex) data...")
        enriched = self.enrich_paper_data(parsed)
        
        for paper in enriched:
            ref_id = paper.get("ref_id")
            if ref_id and ref_id in ref_mentions:
                paper["reference_mentions"] = ref_mentions[ref_id]
        
        print("DEBUG: Assigning entity keys for authors, citations, and venues...")
        enriched, entity_keys = self.assign_entity_keys(enriched)
        
        self._save_results(enriched, output_file)
        entity_keys_file = output_file.replace("enriched_papers.json", "entity_keys.json")
        self._save_results(entity_keys, entity_keys_file)
        print("DEBUG: Processing complete. Results saved to", output_file, "and", entity_keys_file)

    def retry_api_call(self, func, *args):
        """Retry mechanism for API calls"""
        attempts = 0
        while attempts < self.max_retries:
            result = func(*args)
            if result:
                return result
            attempts += 1
            print(f"DEBUG: Retry attempt {attempts} for API call with args: {args}")
            sleep(self.request_delay)
        return None

    def _save_results(self, results, output_file):
        """Save results to a JSON file"""
        print("DEBUG: Saving results to", output_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("DEBUG: Results saved successfully.")

    def search_paper(self, title):
        """Search Semantic Scholar for the paper by title and return the first result's paperId"""
        print("DEBUG: Searching Semantic Scholar for title:", title)
        search_url = f"{self.s2_base}/paper/search"
        params = {
            "query": title,
            "fields": "paperId,title,venue,year,authors",
            "limit": 1  # Only get the first result
        }
        try:
            response = requests.get(search_url, params=params, timeout=15)
            print("DEBUG: Semantic Scholar search response status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                first_paper = data["data"][0]
                print("DEBUG: Found paper via title search:", first_paper)
                return first_paper["paperId"]
            else:
                print("DEBUG: No results found for title search.")
                return None
        except Exception as e:
            print("DEBUG: search_paper error:", e)
            return None

if __name__ == "__main__":
    processor = PaperProcessor()
    processor.process_papers("outputs/rawreferences.txt", "outputs/enriched_papers.json", "outputs/reference_mentions.json")
