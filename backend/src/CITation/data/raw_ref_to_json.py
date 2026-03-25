import requests
from time import sleep
import os
from openai import OpenAI
import json
from .utils import get_openalex_authors, get_openalex_refs
from typing import Literal

# TODO: Make agnostic to LLM choice
# also, is using an LLM really the best way to do this?
# could we not just do this programatically?
# even if it is the best way to do it, do we need to run the LLM on each entry separately?
# would not just throwing the entire dict at the LLM work fine?

OPENALEX_URL = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1"
# https://api.semanticscholar.org/api-docs
OPENALEX_CHUNK_SIZE = 100

# TODO: Use Pydantic to type and validate the metadata we're getting
MetadataSource = Literal["S2", "OpenAlex"] | None


# warns the user that the references for the paper cannot be extracted
# TODO: ask user for location on disk or skip missing reference.
def missing_reference_callback_debug(x):
    print(f"References for paper {x} cannot be extracted. Missing PDF.")


class PaperProcessor:
    def __init__(
        self,
        client,
        max_retries=3,
        request_delay=1,
        missing_ref_callback=missing_reference_callback_debug,
    ):
        self.max_retries = max_retries
        self.request_delay = request_delay
        self.missing_ref_callback = missing_ref_callback
        self.gpt_client = client

        if "S2_API_KEY" in os.environ and os.getenv("S2_API_KEY") != "":
            self.s2_api_key = os.getenv("S2_API_KEY")
        else:
            self.s2_api_key = None
        self.author_map = {}  # (identifier_type, identifier) -> {"author": dict, "key": str}
        self.author_counter = 1

        # Predefined mapping for fake paper authors
        self.fake_author_mapping = {
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
            "D. Vader": "Darth Vader",
        }

        print(
            "DEBUG: Initialized PaperProcessor with Semantic Scholar base URL:",
            SEMANTIC_SCHOLAR_URL,
        )
        if self.s2_api_key:
            print("DEBUG: Semantic Scholar API key loaded successfully.")
        else:
            print("WARNING: No semantic scholar API key provided.")
            # raise ValueError("No Semantic Scholar API key provided!")

    # TODO: can we do this either programatically or as one call?
    # well, each paper should always have a title at least right?
    # if we can reliably extract titles from the text, we can search semantic scholar first
    # then check for the abstract. if the abstract contains a DOI link, we scrape it and give it to
    # chatgpt, or maybe we'll get lucky and get the abstract right off the bat
    # if not, default to using this instead
    def parse_reference_with_gpt(self, ref_text):
        prompt = f"""
Parse this academic reference into JSON format with the following keys: authors (array), title, venue, raw_venue, year, pages, arxiv_id, doi and abstract.
If the venue name in the reference appears abbreviated, expand it to its full name and save the expanded version in "venue",
while preserving the original text in "raw_venue". Use the DOI or axiv link to extract the abstract for the reference. If you are unable to find the abstract using the DOI, search for it using the title in Google Scholar. If you are still unable to find the abstract, please return the reason why in the JSON field for the abstract. DO NOT summarize the paper, return only the abstract verbatim. Handle incomplete information using null for missing fields.

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
  "doi": "10.1234/abcd",
  "abstract": "Lorem ipsum..."
}}
"""

        print("DEBUG: Sending GPT prompt for reference:", ref_text)
        try:
            response = self.gpt_client.responses.create(
                model="gpt-4o-mini",
                tools=[{"type": "web_search"}],
                input=f"{prompt}\n\nReturn ONLY valid JSON as a plain text string without formatting.",
            )
            gpt_output = response.output_text
            print("DEBUG: Received GPT response:", gpt_output)
            result = json.loads(gpt_output)
            if "authors" in result:
                result["authors"] = [
                    author
                    for author in result["authors"]
                    if "et al" not in author.lower()
                ]
            return result
        except Exception as e:
            print(
                f"DEBUG: GPT parsing failed for reference: {ref_text} with error: {e}"
            )
            return None

    def load_and_parse_input(self, references):
        print(f"DEBUG: Found {len(references)} references in the input file")
        parsed_papers = []
        for idx, ref in enumerate(references, 1):
            print(f"DEBUG: Parsing reference {idx}: {ref}")
            paper_data = self.parse_reference_with_gpt(ref)
            if paper_data:
                print(f"DEBUG: Successfully parsed reference {idx}")
                paper_data["ref_id"] = idx
                parsed_papers.append(paper_data)
                # sleep(1)
            else:
                print(f"DEBUG: Failed to parse reference {idx}: {ref}")
        return parsed_papers

    def search_paper(self, title: str):
        """Given a paper title, tries to find its entry in semantic scholar.
        Sadly, this API endpoint only gives a small amount of all of the data we need,
        so we hit their API again with the paperID.

        Args:
            title: Title of the paper.
        """
        print("DEBUG: Searching Semantic Scholar for title:", title)
        # https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_title_search

        search_url = f"{SEMANTIC_SCHOLAR_URL}/paper/search/match"
        params = {
            "query": title,
            "fields": "paperId,title,venue,year,authors",
            "limit": 1,
        }
        try:
            response = requests.get(
                search_url,
                params=params,
                headers={"x-api-key": self.s2_api_key},
                timeout=15,
            )
            print(
                "DEBUG: Semantic Scholar search response status:", response.status_code
            )
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

    def get_paper_details(self, paper_id):
        fields = (
            "title,authors.name,authors.authorId,authors.externalIds,"
            "venue,year,citationCount,fieldsOfStudy,externalIds,paperId,openAccessPdf,references"
        )
        print(f"DEBUG: Fetching Semantic Scholar details for paper ID: {paper_id}")
        try:
            response = requests.get(
                f"{SEMANTIC_SCHOLAR_URL}/paper/{paper_id}",
                params={"fields": fields},
                headers={"x-api-key": self.s2_api_key},
                timeout=15,
            )
            print("DEBUG: Semantic Scholar API response status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            print("DEBUG: Received Semantic Scholar data:", data)
            pdf_data = data.get("openAccessPdf", None)
            data["pdf_url"] = None
            if pdf_data is not None:
                if data["openAccessPdf"]["url"] != "":
                    data["pdf_url"] = data["openAccessPdf"]["url"]

            return data
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: API request failed for paper ID {paper_id}: {e}")
            return None

    def get_paper_details_openalex(self, title):
        params = {"filter": f"title.search:{title}", "per-page": 1}
        print(f"DEBUG: Fetching OpenAlex details for title: {title}")
        try:
            response = requests.get(OPENALEX_URL, params=params, timeout=15)
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

    def _merge_authors(self, parsed_authors, s2_authors, openalex_authors=None):
        """
        Merge author lists, reusing entity keys if ORCID, s2_id, raw_name, or name matches.
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

            name = api_author.get("name")
            s2_id = api_author.get("authorId")
            orcid = None
            if api_author:
                ext_ids = api_author.get("externalIds") or {}
                orcid = ext_ids.get("ORCID")
            if not orcid and openalex_authors and i < len(openalex_authors):
                orcid = openalex_authors[i].get("orcid")

            # Use fake author mapping if raw_name exists and no API name
            mapped_name = (
                self.fake_author_mapping.get(raw_name)
                if raw_name and not name
                else name
            )

            # Create a candidate author dictionary
            candidate = {
                "name": mapped_name or raw_name,
                "s2_id": s2_id,
                "orcid": orcid,
                "raw_name": raw_name,
            }

            # Check for existing author by ORCID, s2_id, raw_name, or name
            author_key = None
            for identifier_type, identifier in [
                ("orcid", orcid),
                ("s2_id", s2_id),
                ("raw_name", raw_name),
                ("name", candidate["name"]),
            ]:
                if identifier and (identifier_type, identifier) in self.author_map:
                    author_key = self.author_map[(identifier_type, identifier)]["key"]
                    existing_author = self.author_map[(identifier_type, identifier)][
                        "author"
                    ]
                    existing_author["name"] = (
                        candidate["name"] or existing_author["name"]
                    )
                    existing_author["s2_id"] = (
                        candidate["s2_id"] or existing_author["s2_id"]
                    )
                    existing_author["orcid"] = (
                        candidate["orcid"] or existing_author["orcid"]
                    )
                    existing_author["raw_name"] = (
                        candidate["raw_name"] or existing_author["raw_name"]
                    )
                    break

            # If no match, create a new author entity
            if not author_key:
                author_key = f"author-{self.author_counter}"
                self.author_counter += 1
                # Register under all available identifiers
                if orcid:
                    self.author_map[("orcid", orcid)] = {
                        "author": candidate,
                        "key": author_key,
                    }
                if s2_id:
                    self.author_map[("s2_id", s2_id)] = {
                        "author": candidate,
                        "key": author_key,
                    }
                if raw_name:
                    self.author_map[("raw_name", raw_name)] = {
                        "author": candidate,
                        "key": author_key,
                    }
                if candidate["name"]:
                    self.author_map[("name", candidate["name"])] = {
                        "author": candidate,
                        "key": author_key,
                    }

            merged_authors.append(author_key)

        print("DEBUG: Merged authors (keys):", merged_authors)
        return merged_authors

    def enrich_paper_data(self, parsed_data):
        print("DEBUG: Starting enrichment of GPT parsed data")
        enriched = []
        for i, paper in enumerate(parsed_data, 1):
            title = paper.get("title")
            if not title:
                print(f"DEBUG: Paper {i} has no title. Skipping enrichment.")
                continue

            skip_apis = "artificial reference paper" in title.lower()
            if skip_apis:
                print(
                    f"DEBUG: Paper {i} with title '{title}' detected as artificial. Skipping APIs."
                )
                enriched_paper = {
                    "title": paper.get("title"),
                    "authors": self._format_authors(paper.get("authors", [])),
                    "year": paper.get("year"),
                    "venue": paper.get("venue"),
                    "raw_venue": paper.get("raw_venue"),
                    "citation_count": 0,
                    "fields_of_study": [],
                    "external_ids": {},
                    "semantic_scholar_id": None,
                    "arxiv_id": paper.get("arxiv_id"),
                    "doi": paper.get("doi"),
                    "ref_id": paper.get("ref_id"),
                    "is_artificial": True,
                    "abstract": "This is not a real paper.",
                }
                enriched.append(enriched_paper)
                continue

            print(
                f"DEBUG: Searching Semantic Scholar for paper {i} with title: {title}"
            )
            # this gets the paper id from semantic scholar, but we need to hit their API again for the rest of the metadata.
            paper_id = self.search_paper(title)

            s2_data = None
            if paper_id:
                print(f"DEBUG: Found paper ID {paper_id} for paper {i}")
                sleep(self.request_delay)
                s2_data = self.retry_api_call(self.get_paper_details, paper_id)
            else:
                print(
                    f"DEBUG: No paper found in Semantic Scholar for paper {i} with title: {title}"
                )

            # we use openalex if 1. we don't have any data 2. we need references or 3. the authors aren't formatted correctly.
            need_openalex_for_authors = False
            need_openalex_for_refs = False
            if s2_data and "authors" in s2_data:
                for author in s2_data.get("authors", []):
                    orcid = (author.get("externalIds") or {}).get("ORCID")
                    if not orcid:
                        need_openalex_for_authors = True
                        break
                if not s2_data.get("references"):
                    # and s2_data.get("pdf_url") is None:
                    # originally thought we rely on reading the pdf for references, but openalex is pretty robust wrt refs
                    need_openalex_for_refs = True

            openalex_data = None
            openalex_authors = None
            openalex_refs = None
            if not s2_data or need_openalex_for_authors or need_openalex_for_refs:
                print(
                    f"DEBUG: ORCID missing or Semantic Scholar data not available for paper {i}, attempting OpenAlex..."
                )
                openalex_data = self.get_paper_details_openalex(title)
                if openalex_data:
                    if need_openalex_for_authors:
                        openalex_authors = get_openalex_authors(openalex_data)

                    if need_openalex_for_refs:
                        openalex_refs = get_openalex_refs(openalex_data)

            if s2_data:
                merged = self._merge_data(
                    paper, s2_data, openalex_authors, openalex_refs
                )
                merged["is_artificial"] = False
                print(f"DEBUG: Merged data for paper {i}: {merged}")
                enriched.append(merged)
            elif openalex_data:
                merged = self._merge_data_openalex(paper, openalex_data)
                merged["is_artificial"] = False
                print(f"DEBUG: Merged OpenAlex data for paper {i}: {merged}")
                enriched.append(merged)
            else:
                print(
                    f"DEBUG: No data found for paper {i} on either Semantic Scholar or OpenAlex."
                )
                enriched_paper = self._format_gpt_only(paper)
                enriched_paper["is_artificial"] = False
                enriched.append(enriched_paper)
            sleep(self.request_delay)
        return enriched

    def _format_gpt_only(self, paper):
        return {
            "title": paper.get("title"),
            "authors": self._format_authors(paper.get("authors", [])),
            "year": paper.get("year"),
            "venue": paper.get("venue"),
            "raw_venue": paper.get("raw_venue"),
            "citation_count": 0,
            "fields_of_study": [],
            "external_ids": {},
            "semantic_scholar_id": None,
            "arxiv_id": paper.get("arxiv_id"),
            "doi": paper.get("doi"),
            "ref_id": paper.get("ref_id"),
            "abstract": paper.get("abstract"),
        }

    def _format_authors(self, authors):
        """Format authors for GPT-only cases, reusing entity keys."""
        formatted = []
        for raw_name in authors:
            mapped_name = self.fake_author_mapping.get(raw_name, raw_name)
            if ("raw_name", raw_name) in self.author_map:
                author_key = self.author_map[("raw_name", raw_name)]["key"]
                existing_author = self.author_map[("raw_name", raw_name)]["author"]
                existing_author["name"] = mapped_name or existing_author["name"]
            elif ("name", mapped_name) in self.author_map:
                author_key = self.author_map[("name", mapped_name)]["key"]
                existing_author = self.author_map[("name", mapped_name)]["author"]
                existing_author["raw_name"] = raw_name or existing_author["raw_name"]
            else:
                author_key = f"author-{self.author_counter}"
                self.author_counter += 1
                author_dict = {
                    "name": mapped_name,
                    "s2_id": None,
                    "orcid": None,
                    "raw_name": raw_name,
                }
                self.author_map[("raw_name", raw_name)] = {
                    "author": author_dict,
                    "key": author_key,
                }
                self.author_map[("name", mapped_name)] = {
                    "author": author_dict,
                    "key": author_key,
                }
            formatted.append(author_key)
        return formatted

    def _merge_data(self, parsed, s2, openalex_authors=None, openalex_refs=None):
        venue_full = parsed.get("venue") if "venue" in parsed else s2.get("venue")
        raw_venue = (
            parsed.get("raw_venue")
            if "raw_venue" in parsed
            else s2.get("venue", parsed.get("venue"))
        )

        refs = None
        ref_source = None
        if s2.get("references"):
            refs = s2["references"]
            ref_source = "s2"
        elif openalex_refs:
            refs = openalex_refs
            ref_source = "openalex"

        """
        if refs is None and s2.get("pdf_url") is None:
            # TODO: add ability to upload pdfs during this process
            print(
                f"WARNING: Could not extract references nor locate PDF for {s2.get('title', parsed.get('title'))}."
            )
        """

        merged = {
            "title": s2.get("title", parsed.get("title")),
            "abstract": parsed.get("abstract"),
            "authors": self._merge_authors(
                parsed.get("authors", []), s2.get("authors", []), openalex_authors
            ),
            "year": s2.get("year", parsed.get("year")),
            "venue": venue_full,
            "raw_venue": raw_venue,
            "citation_count": s2.get("citationCount", 0),
            "fields_of_study": s2.get("fieldsOfStudy", []),
            "external_ids": s2.get("externalIds", {}),
            "semantic_scholar_id": s2.get("paperId"),
            "references": refs,
            "ref_source": ref_source,
            "pdf_url": s2.get("pdf_url", None),
            "arxiv_id": parsed.get("arxiv_id"),
            "doi": s2.get("externalIds", {}).get("DOI", parsed.get("doi")),
        }
        if "ref_id" in parsed:
            merged["ref_id"] = parsed["ref_id"]
        print("DEBUG: _merge_data output:", merged)
        return merged

    def _merge_data_openalex(self, parsed, openalex):
        title = openalex.get("display_name", parsed.get("title"))
        openalex_authors = get_openalex_authors(openalex)
        refs = get_openalex_refs(openalex)
        ref_source = "openalex" if refs is not None else None

        venue_full = (
            parsed.get("venue")
            if "venue" in parsed
            else openalex.get("host_venue", {}).get("display_name")
        )
        raw_venue = (
            parsed.get("raw_venue")
            if "raw_venue" in parsed
            else openalex.get("host_venue", {}).get("display_name", parsed.get("venue"))
        )

        merged = {
            "title": title,
            "authors": self._merge_authors(
                parsed.get("authors", []), [], openalex_authors
            ),
            "year": openalex.get("publication_year", parsed.get("year")),
            "venue": venue_full,
            "raw_venue": raw_venue,
            "citation_count": openalex.get("citation_count", 0),
            "fields_of_study": openalex.get("concepts", []),
            "external_ids": {"OpenAlex": openalex.get("id")},
            "references": refs,
            "ref_source": ref_source,
            "semantic_scholar_id": None,
            "pdf_url": None,
            "arxiv_id": parsed.get("arxiv_id"),
            "abstract": parsed.get("abstract"),
            "doi": openalex.get("doi", parsed.get("doi")),
        }
        if "ref_id" in parsed:
            merged["ref_id"] = parsed["ref_id"]
        print("DEBUG: _merge_data_openalex output:", merged)
        return merged

    def assign_entity_keys(self, enriched):
        d = {}
        entity_keys = {
            "authors": {v["key"]: v["author"] for v in self.author_map.values()},
            "citations": {},
            "venues": {},
        }
        venue_key_map = {}
        venue_counter = 1
        citation_counter = 1

        for paper in enriched:
            citation_key = f"citation-{citation_counter}"
            citation_counter += 1
            paper["citation_key"] = citation_key
            entity_keys["citations"][citation_key] = paper

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
            paper["hop"] = 1
            d[paper["ref_id"]] = paper
        return d, entity_keys

    def retry_api_call(self, func, *args):
        attempts = 0
        while attempts < self.max_retries:
            result = func(*args)
            if result:
                return result
            attempts += 1
            print(f"DEBUG: Retry attempt {attempts} for API call with args: {args}")
            sleep(self.request_delay)
        return None

    def process_papers(self, raw_references, ref_mentions):
        print("DEBUG: Starting processing of papers")
        print("DEBUG: Parsing input file with GPT...")
        parsed = self.load_and_parse_input(raw_references)

        print("DEBUG: Enriching data...")
        enriched = self.enrich_paper_data(parsed)

        # process second hops here
        for paper in enriched:
            ref_id = paper.get("ref_id")
            if ref_id and ref_id in ref_mentions:
                paper["reference_mentions"] = ref_mentions[ref_id]
            enriched_refs = self.process_second_hops(paper)
            paper["enriched_references"] = enriched_refs

        # build dict of entity keys
        print("DEBUG: Assigning entity keys...")
        enriched, entity_keys = self.assign_entity_keys(enriched)
        # TODO: probably make this into one function
        enriched, entity_keys = self.assign_entity_keys_with_refs(enriched, entity_keys)

        return enriched, entity_keys

    def get_openalex_work_details(self, work_ids):
        """Fetch details for multiple openalex works by ID."""
        # can batch with ?filter=ids.openalex:{id1}|{id2}|{id3}...
        url = f"{OPENALEX_URL}?filter=ids.openalex:"
        for i, x in enumerate(work_ids):
            work_id_short = x.split("/")[-1]
            url += str(work_id_short)
            if i != len(work_ids) - 1:
                url += "|"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            print(f"DEBUG: Received OpenAlex work details for {url}:", data)
            return data["results"]
        except Exception as e:
            print(f"DEBUG: Error fetching OpenAlex work details for {url}: {e}")
            return None

    def _merge_ref_authors(
        self, s2_authors=None, openalex_authors=None, is_artificial_parent=False
    ):
        """Merge author lists, applying nameMap for artificial parent papers."""
        if s2_authors is None and openalex_authors is None:
            return []
        merged_authors = []
        authors = s2_authors if s2_authors is not None else openalex_authors
        max_length = len(authors) if authors else 0
        for i in range(max_length):
            api_author = authors[i] if i < len(authors) else {}
            name = api_author.get("name")
            s2_id = api_author.get("authorId") if s2_authors else None
            orcid = None
            if api_author:
                ext_ids = api_author.get("externalIds") or {}
                orcid = ext_ids.get("ORCID")
            if not orcid and openalex_authors and i < len(openalex_authors):
                orcid = openalex_authors[i].get("orcid")
            # Apply nameMap for artificial parent papers
            mapped_name = (
                self.fake_author_mapping.get(name, name)
                if is_artificial_parent and name
                else name
            )
            merged_authors.append(
                {"name": mapped_name, "s2_id": s2_id, "orcid": orcid, "raw_name": name}
            )
        print("DEBUG: Merged authors:", merged_authors)
        return merged_authors

    # this can really be one function I think, but for now we'll do it the old way
    def assign_entity_keys_with_refs(self, references_data, entity_keys):
        """Assign unique keys, merging authors by raw_name and name for artificial parent papers."""
        author_key_map = {}  # (name_lower, orcid) or (raw_name) -> {"author": dict, "key": str}
        venue_key_map = {v: k for k, v in entity_keys["venues"].items()}

        doi_map = {}
        openalex_map = {}
        s2_map = {}
        title_map = {}

        existing_citation_ids = [
            int(k.split("-")[1])
            for k in entity_keys["citations"].keys()
            if k.startswith("citation-")
        ]
        citation_counter = (
            max(existing_citation_ids) + 1 if existing_citation_ids else 1
        )
        author_counter = (
            max([int(k.split("-")[1]) for k in entity_keys["authors"].keys()] + [0]) + 1
        )
        venue_counter = (
            max([int(k.split("-")[1]) for k in entity_keys["venues"].keys()] + [0]) + 1
        )

        # Populate existing author and citation maps
        for a_key, author in entity_keys["authors"].items():
            name_lower = author.get("name", "").lower().strip()
            orcid = author.get("orcid")
            raw_name = author.get("raw_name")
            if name_lower and orcid:
                author_key_map[(name_lower, orcid)] = {"author": author, "key": a_key}
            elif raw_name:
                author_key_map[("raw_name", raw_name)] = {
                    "author": author,
                    "key": a_key,
                }

        for citation_key, citation_data in entity_keys["citations"].items():
            ext_ids = citation_data.get("external_ids", {})
            doi = ext_ids.get("DOI")
            openalex_id = ext_ids.get("OpenAlex")
            s2_id = citation_data.get("semantic_scholar_id")
            title_lower = (
                citation_data.get("title", "").lower().strip()
                if citation_data.get("title") is not None
                else ""
            )
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
            enriched_refs = data.get("enriched_references", None)
            if enriched_refs is None:
                continue
            for ref in enriched_refs:
                new_authors = []
                for author in ref.get("authors", []):
                    name = author.get("name", "").strip()
                    raw_name = author.get("raw_name")
                    orcid = author.get("orcid")
                    s2_id = author.get("s2_id")

                    # Apply nameMap for artificial parent papers
                    if is_artificial_parent and raw_name:
                        name = self.fake_author_mapping.get(raw_name, raw_name)

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
                            author_key_map[(name_lower, orcid)] = {
                                "author": existing,
                                "key": author_key,
                            }
                    elif name_lower and name_lower in [
                        k[0] for k in author_key_map.keys() if k[0] != "raw_name"
                    ]:
                        for (k_type, k_value), v in author_key_map.items():
                            if (
                                k_type != "raw_name"
                                and k_value == name_lower
                                and not v["author"].get("orcid")
                            ):
                                author_key = v["key"]
                                existing = v["author"]
                                existing["raw_name"] = raw_name or existing["raw_name"]
                                existing["s2_id"] = s2_id or existing["s2_id"]
                                existing["orcid"] = orcid or existing["orcid"]
                                if orcid:
                                    author_key_map[(name_lower, orcid)] = {
                                        "author": existing,
                                        "key": author_key,
                                    }
                                break

                    if not author_key:
                        author_key = f"author-{author_counter}"
                        author["name"] = name
                        author["key"] = author_key
                        if name_lower and orcid:
                            author_key_map[(name_lower, orcid)] = {
                                "author": author,
                                "key": author_key,
                            }
                        if raw_name:
                            author_key_map[("raw_name", raw_name)] = {
                                "author": author,
                                "key": author_key,
                            }
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
                title_lower = (
                    ref.get("title", "").lower().strip()
                    if ref.get("title") is not None
                    else ""
                )

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
                    print(
                        f"DEBUG: Reusing existing citation key {citation_key} for {ref.get('title')}"
                    )
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
                        "hop": 2,
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

    # same here, this likely can be the logic for merge_data
    def _merge_ref_data(self, s2=None, openalex=None, is_artificial_parent=False):
        """Merge Semantic Scholar or OpenAlex data, applying nameMap for artificial parent papers."""
        if s2:
            merged = {
                "title": s2.get("title"),
                "authors": self._merge_ref_authors(
                    s2_authors=s2.get("authors", []),
                    is_artificial_parent=is_artificial_parent,
                ),
                "year": s2.get("year"),
                "venue": s2.get("venue"),
                "citation_count": s2.get("citationCount", 0),
                "fields_of_study": s2.get("fieldsOfStudy", []),
                "external_ids": s2.get("externalIds", {}),
                "semantic_scholar_id": s2.get("paperId"),
                "arxiv_id": None,
                "doi": s2.get("externalIds", {}).get("DOI"),
            }
        elif openalex:
            merged = {
                "title": openalex.get("title"),
                "authors": self._merge_ref_authors(
                    openalex_authors=[
                        {
                            "name": a["author"]["display_name"],
                            "externalIds": {"ORCID": a["author"]["orcid"]},
                        }
                        for a in openalex.get("authorships", [])
                    ],
                    is_artificial_parent=is_artificial_parent,
                ),
                "year": openalex.get("publication_year"),
                "venue": openalex.get("host_venue", {}).get("display_name"),
                "citation_count": openalex.get("cited_by_count", 0),
                "fields_of_study": [
                    c["display_name"] for c in openalex.get("concepts", [])
                ],
                "external_ids": {
                    "DOI": openalex.get("doi"),
                    "OpenAlex": openalex.get("id"),
                },
                "semantic_scholar_id": None,
                "arxiv_id": None,
                "doi": openalex.get("doi"),
            }
        else:
            merged = {}
        print("DEBUG: _merge_data output:", merged)
        return merged

    def process_second_hops(self, paper):
        if paper["is_artificial"]:
            return []

        refs = paper["references"]
        ref_source = paper["ref_source"]
        pdf_url = paper["pdf_url"]
        title = paper.get("title")

        enriched_refs = []
        if not refs:
            if pdf_url is None:
                self.missing_ref_callback(paper)
            else:
                # TODO: download the PDF URL and extract references automatically
                self.missing_ref_callback(paper)
            return []

        if ref_source == "openalex":
            chunks = [
                refs[i : i + OPENALEX_CHUNK_SIZE] for i in range(0, len(refs), 25)
            ]
            for chunk in chunks:
                details = self.retry_api_call(self.get_openalex_work_details, chunk)
                for d in details:
                    merged = self._merge_ref_data(
                        openalex=d,
                        is_artificial_parent="artificial paper" in title.lower(),
                    )
                    enriched_refs.append(merged)

        for ref in refs:
            if ref_source == "s2":
                details = self.retry_api_call(self.get_paper_details, ref)
                if details:
                    merged = self._merge_ref_data(
                        s2=details,
                        is_artificial_parent="artificial paper" in title.lower(),
                    )
                else:
                    print(
                        f"DEBUG: Semantic Scholar failed for {ref}, skipping reference."
                    )
                    continue

            sleep(self.request_delay)
        return enriched_refs
