import requests
import json
from time import sleep
import os
import re
import PyPDF2
from openai import OpenAI

class SecondHopProcessor:
    def __init__(self, s2_api_key=None):
        self.s2_base = "https://api.semanticscholar.org/graph/v1"
        self.openalex_base = "https://api.openalex.org/works"
        self.max_retries = 3
        self.request_delay = 1
        self.gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Load the Semantic Scholar API key
        self.s2_api_key = s2_api_key if s2_api_key else os.getenv("S2_API_KEY")
        
        # Name mapping for artificial papers
        self.nameMap = {
            "H. Solo": "Han Solo",
            "L. Skywalker": "Luke Skywalker",
            "O.-W. Kenobi": "Obi-Wan Kenobi",
            "D. Smeesters": "Dirk Smeesters",
            "J. Liu": "Jia Liu",
            "J. Hutt": "Jabba Hutt",
            "L. Organa": "Leia Organa",
            "Q.-G. Jinn": "Qui-Gon Jinn",
            "A. Skywalker": "Anakin Skywalker",
            "M. Windu": "Mace Windu",
            "Chewbacca": "Chewbacca",
            "D. Vader": "Darth Vader"
        }

        print("DEBUG: Initialized SecondHopProcessor with Semantic Scholar base URL:", self.s2_base)
        if self.s2_api_key:
            print("DEBUG: Semantic Scholar API key detected.")
        else:
            print("WARNING: No Semantic Scholar API key provided or found in environment.")
        if not os.getenv("OPENAI_API_KEY"):
            print("WARNING: No OpenAI API key found in environment.")

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
            print(f"DEBUG: Loaded entity keys: {len(entity_keys.get('authors', {}))} authors, "
                  f"{len(entity_keys.get('venues', {}))} venues, "
                  f"{len(entity_keys.get('citations', {}))} citations")
        else:
            entity_keys = {"authors": {}, "citations": {}, "venues": {}}
            print("DEBUG: No existing entity keys file found, starting with empty keys.")
        return entity_keys

    def get_references_for_paper(self, paper_id):
        """Fetch references from Semantic Scholar."""
        fields = "references.paperId,references.title,references.authors,references.venue,references.year"
        url = f"{self.s2_base}/paper/{paper_id}"
        params = {"fields": fields}
        print(f"DEBUG: Fetching references for paper ID: {paper_id}")
        try:
            headers = {"x-api-key": self.s2_api_key} if self.s2_api_key else {}
            response = requests.get(url, params=params, headers=headers, timeout=15)
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
        """Fetch full details from Semantic Scholar."""
        fields = (
            "title,authors.name,authors.authorId,authors.externalIds,"
            "venue,year,citationCount,fieldsOfStudy,externalIds,paperId"
        )
        url = f"{self.s2_base}/paper/{paper_id}"
        params = {"fields": fields}
        print(f"DEBUG: Fetching full details for paper ID: {paper_id}")
        try:
            headers = {"x-api-key": self.s2_api_key} if self.s2_api_key else {}
            response = requests.get(url, params=params, headers=headers, timeout=15)
            print("DEBUG: get_paper_details response status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            print("DEBUG: Received details for paper ID:", paper_id, data)
            return data
        except Exception as e:
            print(f"DEBUG: Error fetching details for paper ID {paper_id}: {e}")
            return None

    def get_paper_details_openalex(self, title):
        """Fetch references from OpenAlex by title."""
        params = {"filter": f"title.search:{title}", "per-page": 1}
        print(f"DEBUG: Fetching OpenAlex details for title: {title}")
        try:
            response = requests.get(self.openalex_base, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                refs = data["results"][0].get("referenced_works", [])
                print(f"DEBUG: Found {len(refs)} referenced works for title: {title}")
                return refs
            else:
                print("DEBUG: No results found on OpenAlex for title:", title)
                return None
        except Exception as e:
            print(f"DEBUG: OpenAlex API request failed for title {title}: {e}")
            return None

    def get_openalex_work_details(self, work_id):
        """Fetch details for an OpenAlex work by ID."""
        work_id_short = work_id.split('/')[-1]
        url = f"{self.openalex_base}/{work_id_short}"
        print(f"DEBUG: Fetching OpenAlex work details for ID: {url}")
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            print(f"DEBUG: Received OpenAlex work details for {url}:", data)
            return data
        except Exception as e:
            print(f"DEBUG: Error fetching OpenAlex work details for {url}: {e}")
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

    def extract_references_from_pdf(self, pdf_path):
        """Extract reference section from a PDF using regex."""
        print(f"DEBUG: Extracting references from PDF: {pdf_path}")
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                
                ref_pattern = r"(References|Bibliography)[\s\S]+?(?=\n\n|\Z)"
                match = re.search(ref_pattern, text, re.IGNORECASE)
                if match:
                    ref_text = match.group(0)
                    ref_lines = re.split(r'\n(?=\[\d+\]|\d+\.\s|\s+[A-Z])', ref_text)[1:]
                    print(f"DEBUG: Found {len(ref_lines)} potential references in {pdf_path}")
                    return [line.strip() for line in ref_lines if line.strip()]
                else:
                    print(f"DEBUG: No references section found in {pdf_path}")
                    return []
        except Exception as e:
            print(f"DEBUG: Error extracting references from {pdf_path}: {e}")
            return []

    def parse_reference_with_gpt(self, ref_text):
        """Parse a reference using GPT."""
        prompt = f"""
Parse this academic reference into JSON format with the following keys: authors (array), title, venue, raw_venue, year, pages, arxiv_id, and doi.
If the venue name appears abbreviated, expand it to its full name and save in "venue", preserving the original in "raw_venue".
Handle incomplete information using null for missing fields. Filter out 'et al.' from authors.

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
            if "authors" in result:
                result["authors"] = [author for author in result["authors"] if "et al" not in author.lower()]
            return result
        except Exception as e:
            print(f"DEBUG: GPT parsing failed for reference: {ref_text} with error: {e}")
            return None

    def process_artificial_paper(self, paper):
        """Pipeline for artificial first-hop papers: extract references from PDF and parse with GPT."""
        ref_id = paper.get("ref_id")
        if not ref_id:
            print(f"DEBUG: No ref_id found for artificial paper '{paper.get('title')}', skipping.")
            return None

        pdf_path = os.path.join("reference_papers", f"{ref_id}.pdf")
        if not os.path.exists(pdf_path):
            print(f"DEBUG: PDF not found at {pdf_path} for artificial paper '{paper.get('title')}', skipping.")
            return None

        ref_lines = self.extract_references_from_pdf(pdf_path)
        if not ref_lines:
            print(f"DEBUG: No references extracted from {pdf_path}, skipping.")
            return None

        enriched_refs = []
        for ref_text in ref_lines:
            ref_data = self.parse_reference_with_gpt(ref_text)
            if ref_data:
                merged = {
                    "title": ref_data.get("title"),
                    "authors": [{"name": self.nameMap.get(author, author), "s2_id": None, "orcid": None, "raw_name": author} 
                                for author in ref_data.get("authors", [])],
                    "year": ref_data.get("year"),
                    "venue": ref_data.get("venue"),
                    "raw_venue": ref_data.get("raw_venue"),
                    "citation_count": 0,
                    "fields_of_study": [],
                    "external_ids": {},
                    "semantic_scholar_id": None,
                    "arxiv_id": ref_data.get("arxiv_id"),
                    "doi": ref_data.get("doi")
                }
                enriched_refs.append(merged)
                sleep(self.request_delay)
            else:
                print(f"DEBUG: Failed to parse reference: {ref_text}")

        return {
            "title": paper.get("title"),
            "references": enriched_refs
        }

    def _merge_authors(self, s2_authors=None, openalex_authors=None, is_artificial_parent=False):
        """Merge author lists, applying nameMap for artificial parent papers."""
        if s2_authors is None and openalex_authors is None:
            return []
        merged_authors = []
        authors = s2_authors if s2_authors is not None else openalex_authors
        max_length = len(authors) if authors else 0
        for i in range(max_length):
            api_author = authors[i] if i < len(authors) else {}
            name = api_author.get('name')
            s2_id = api_author.get('authorId') if s2_authors else None
            orcid = None
            if api_author:
                ext_ids = api_author.get('externalIds') or {}
                orcid = ext_ids.get('ORCID')
            if not orcid and openalex_authors and i < len(openalex_authors):
                orcid = openalex_authors[i].get("orcid")
            # Apply nameMap for artificial parent papers
            mapped_name = self.nameMap.get(name, name) if is_artificial_parent and name else name
            merged_authors.append({
                "name": mapped_name,
                "s2_id": s2_id,
                "orcid": orcid,
                "raw_name": name
            })
        print("DEBUG: Merged authors:", merged_authors)
        return merged_authors

    def _merge_data(self, s2=None, openalex=None, is_artificial_parent=False):
        """Merge Semantic Scholar or OpenAlex data, applying nameMap for artificial parent papers."""
        if s2:
            merged = {
                "title": s2.get('title'),
                "authors": self._merge_authors(s2_authors=s2.get('authors', []), is_artificial_parent=is_artificial_parent),
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
                "authors": self._merge_authors(openalex_authors=[
                    {"name": a["author"]["display_name"], 
                     "externalIds": {"ORCID": a["author"]["orcid"]}}
                    for a in openalex.get("authorships", [])
                ], is_artificial_parent=is_artificial_parent),
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
        """Assign unique keys, merging authors by raw_name and name for artificial parent papers."""
        author_key_map = {}  # (name_lower, orcid) or (raw_name) -> {"author": dict, "key": str}
        venue_key_map = {v: k for k, v in entity_keys["venues"].items()}

        doi_map = {}
        openalex_map = {}
        s2_map = {}
        title_map = {}

        existing_citation_ids = [int(k.split('-')[1]) for k in entity_keys["citations"].keys() if k.startswith("citation-")]
        citation_counter = max(existing_citation_ids) + 1 if existing_citation_ids else 1
        author_counter = max([int(k.split('-')[1]) for k in entity_keys["authors"].keys()] + [0]) + 1
        venue_counter = max([int(k.split('-')[1]) for k in entity_keys["venues"].keys()] + [0]) + 1

        # Populate existing author and citation maps
        for a_key, author in entity_keys["authors"].items():
            name_lower = author.get("name", "").lower().strip()
            orcid = author.get("orcid")
            raw_name = author.get("raw_name")
            if name_lower and orcid:
                author_key_map[(name_lower, orcid)] = {"author": author, "key": a_key}
            elif raw_name:
                author_key_map[("raw_name", raw_name)] = {"author": author, "key": a_key}

        for citation_key, citation_data in entity_keys["citations"].items():
            ext_ids = citation_data.get("external_ids", {})
            doi = ext_ids.get("DOI")
            openalex_id = ext_ids.get("OpenAlex")
            s2_id = citation_data.get("semantic_scholar_id")
            title_lower = citation_data.get("title", "").lower().strip() if citation_data.get("title") is not None else ""
            if doi:
                doi_map[doi] = citation_key
            if openalex_id:
                openalex_map[openalex_id] = citation_key
            if s2_id:
                s2_map[s2_id] = citation_key
            if title_lower:
                title_map[title_lower] = citation_key

        for paper_id, data in references_data.items():
            is_artificial_parent = "artificial paper" in data["title"].lower()
            enriched_refs = data["references"]

            for ref in enriched_refs:
                new_authors = []
                for author in ref.get("authors", []):
                    name = author.get("name", "").strip()
                    raw_name = author.get("raw_name")
                    orcid = author.get("orcid")
                    s2_id = author.get("s2_id")

                    # Apply nameMap for artificial parent papers
                    if is_artificial_parent and raw_name:
                        name = self.nameMap.get(raw_name, raw_name)

                    # Check for existing author by (name, orcid) or raw_name
                    author_key = None
                    name_lower = name.lower() if name else ""
                    if name_lower and orcid and (name_lower, orcid) in author_key_map:
                        author_key = author_key_map[(name_lower, orcid)]["key"]
                        existing = author_key_map[(name_lower, orcid)]["author"]
                        existing["raw_name"] = raw_name or existing["raw_name"]
                        existing["s2_id"] = s2_id or existing["s2_id"]
                    elif raw_name and ("raw_name", raw_name) in author_key_map:
                        author_key = author_key_map[("raw_name", raw_name)]["key"]
                        existing = author_key_map[("raw_name", raw_name)]["author"]
                        existing["name"] = name or existing["name"]
                        existing["s2_id"] = s2_id or existing["s2_id"]
                        existing["orcid"] = orcid or existing["orcid"]
                        if name_lower and orcid:
                            author_key_map[(name_lower, orcid)] = {"author": existing, "key": author_key}
                    elif name_lower and name_lower in [k[0] for k in author_key_map.keys() if k[0] != "raw_name"]:
                        for (k_type, k_value), v in author_key_map.items():
                            if k_type != "raw_name" and k_value == name_lower and not v["author"].get("orcid"):
                                author_key = v["key"]
                                existing = v["author"]
                                existing["raw_name"] = raw_name or existing["raw_name"]
                                existing["s2_id"] = s2_id or existing["s2_id"]
                                existing["orcid"] = orcid or existing["orcid"]
                                if orcid:
                                    author_key_map[(name_lower, orcid)] = {"author": existing, "key": author_key}
                                break

                    if not author_key:
                        author_key = f"author-{author_counter}"
                        author["name"] = name
                        author["key"] = author_key
                        if name_lower and orcid:
                            author_key_map[(name_lower, orcid)] = {"author": author, "key": author_key}
                        if raw_name:
                            author_key_map[("raw_name", raw_name)] = {"author": author, "key": author_key}
                        entity_keys["authors"][author_key] = author
                        author_counter += 1

                    new_authors.append(author_key)
                ref["authors"] = new_authors

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

                ext_ids = ref.get("external_ids", {})
                doi = ext_ids.get("DOI")
                openalex_id = ext_ids.get("OpenAlex")
                s2_id = ref.get("semantic_scholar_id")
                title_lower = ref.get("title", "").lower().strip() if ref.get("title") is not None else ""

                existing_key = None
                if doi and doi in doi_map:
                    existing_key = doi_map[doi]
                elif openalex_id and openalex_id in openalex_map:
                    existing_key = openalex_map[openalex_id]
                elif s2_id and s2_id in s2_map:
                    existing_key = s2_map[s2_id]
                elif title_lower and title_lower in title_map:
                    existing_key = title_map[title_lower]

                if existing_key:
                    citation_key = existing_key
                    print(f"DEBUG: Reusing existing citation key {citation_key} for {ref.get('title')}")
                else:
                    citation_key = f"citation-{citation_counter}"
                    citation_counter += 1
                    entity_keys["citations"][citation_key] = {
                        "title": ref.get("title", ""),
                        "authors": ref["authors"],
                        "venue": ref["venue"],
                        "year": ref["year"],
                        "citation_count": ref.get("citation_count", 0),
                        "fields_of_study": ref.get("fields_of_study", []),
                        "external_ids": ref.get("external_ids", {}),
                        "semantic_scholar_id": ref.get("semantic_scholar_id"),
                        "arxiv_id": ref.get("arxiv_id"),
                        "doi": ref["doi"],
                        "second_hop": "yes"
                    }
                    if doi:
                        doi_map[doi] = citation_key
                    if openalex_id:
                        openalex_map[openalex_id] = citation_key
                    if s2_id:
                        s2_map[s2_id] = citation_key
                    if title_lower:
                        title_map[title_lower] = citation_key

                ref["citation_key"] = citation_key

        return references_data, entity_keys


    def process_second_hop(self, input_file, output_file, entity_keys_file):
        """Process second-hop references with special handling for artificial papers."""
        papers = self.load_enriched_papers(input_file)
        entity_keys = self.load_entity_keys(entity_keys_file)
        all_references = {}

        for idx, paper in enumerate(papers, 1):
            title = paper.get("title")
            if not title:
                print(f"DEBUG: Paper {idx} has no title. Skipping second hop.")
                continue
            print(f"DEBUG: Processing second hop for paper {idx} with title: {title}")

            if paper.get("is_artificial", False):
                result = self.process_artificial_paper(paper)
                if result:
                    all_references[title] = result
                else:
                    print(f"DEBUG: Failed to process artificial paper '{title}', skipping.")
            else:
                paper_id = paper.get("semantic_scholar_id")
                if paper_id:
                    refs = self.retry_api_call(self.get_references_for_paper, paper_id)
                    source = "Semantic Scholar"
                else:
                    print(f"DEBUG: No Semantic Scholar ID for paper {idx}, using OpenAlex title search")
                    openalex_refs = self.retry_api_call(self.get_paper_details_openalex, title)
                    if openalex_refs is None:
                        print(f"DEBUG: OpenAlex failed to fetch references for title {title}, skipping.")
                        continue
                    refs = [{"paperId": ref} for ref in openalex_refs]
                    source = "OpenAlex"

                if refs is None:
                    print(f"DEBUG: Failed to fetch references for paper {idx}, skipping.")
                    continue

                enriched_refs = []
                for ref in refs:
                    ref_paper_id = ref.get("paperId")
                    if not ref_paper_id:
                        print("DEBUG: Reference without paperId, skipping")
                        continue
                    print(f"DEBUG: Enriching reference with paperId: {ref_paper_id}")

                    if source == "Semantic Scholar":
                        details = self.retry_api_call(self.get_paper_details, ref_paper_id)
                        if details:
                            merged = self._merge_data(s2=details, is_artificial_parent="artificial paper" in title.lower())
                        else:
                            print(f"DEBUG: Semantic Scholar failed for {ref_paper_id}, skipping reference")
                            continue
                    else:
                        details = self.retry_api_call(self.get_openalex_work_details, ref_paper_id)
                        if details:
                            merged = self._merge_data(openalex=details, is_artificial_parent="artificial paper" in title.lower())
                        else:
                            print(f"DEBUG: OpenAlex failed for work ID {ref_paper_id}, skipping reference")
                            continue

                    enriched_refs.append(merged)
                    sleep(self.request_delay)

                all_references[paper_id or title] = {
                    "title": title,
                    "references": enriched_refs
                }

        all_references, entity_keys = self.assign_entity_keys(all_references, entity_keys)

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
        "outputs/enriched_papers_with_bboxes.json",
        "outputs/second_hop_references.json",
        "outputs/entity_keys.json"
    )