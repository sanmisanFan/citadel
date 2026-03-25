from .datatypes import PaperMetadata
from collections import defaultdict


def extract_info(entity_keys, new_paper: PaperMetadata):
    citations = entity_keys["citations"]

    author_citations = {}
    author_venues = {}
    for citation_key, citation in citations.items():
        for author_id in citation["authors"]:
            if author_id not in author_citations:
                author_citations[author_id] = []
            author_citations[author_id].append(citation_key)
            if citation["venue"]:
                if author_id not in author_venues:
                    author_venues[author_id] = []
                if citation["venue"] not in author_venues[author_id]:
                    author_venues[author_id].append(citation["venue"])

    authors = []
    for author_id, author_data in entity_keys["authors"].items():
        author_obj = {
            "id": author_id,
            "raw_name": author_data.get("raw_name", author_data.get("name", "")),
            "standardized_name": author_data.get("name", ""),
            "openalex_link": None,
            "orcid": author_data.get("orcid", None),
            "citation": author_citations.get(author_id, []),
            "venue": author_venues.get(author_id, []),
            "author_graph": [],
        }
        authors.append(author_obj)

    venue_data = {}
    for venue_id, standardized_name in entity_keys["venues"].items():
        venue_data[venue_id] = {
            "raw_name": set(),
            "year": set(),
            "author": set(),
            "citation": set(),
            "standardized_name": standardized_name,
        }

    # this goes through the list of citations and tries to group citations by the venue they were published
    for citation_key, citation in citations.items():
        venue_id = citation["venue"]
        if venue_id and venue_id in venue_data:
            venue_data[venue_id]["raw_name"].add(citation.get("raw_venue", ""))
            venue_data[venue_id]["year"].add(str(citation.get("year", "")))
            for author_id in citation["authors"]:
                venue_data[venue_id]["author"].add(author_id)
            venue_data[venue_id]["citation"].add(citation_key)

    for venue_id in venue_data.keys():
        venue_data[venue_id]["raw_name"] = list(venue_data[venue_id]["raw_name"])
        venue_data[venue_id]["year"] = list(venue_data[venue_id]["year"])
        venue_data[venue_id]["author"] = list(venue_data[venue_id]["author"])
        venue_data[venue_id]["citation"] = list(venue_data[venue_id]["citation"])

    # why do this again?
    venues = []
    for venue_id, data in venue_data.items():
        venue_obj = {
            "id": venue_id,
            "type": "Unknown",
            "raw_name": data["raw_name"],
            "short": data["standardized_name"][:10]
            if data["standardized_name"]
            else "Unknown",
            "standardized_name": data["standardized_name"],
            "year": data["year"],
            "author": data["author"],
            "citation": data["citation"],
            "venue_graph": [],
        }
        venues.append(venue_obj)

    # can this be wrapped in a fn that is called for all of the citations we generate?
    new_citation_id = "citation-0"
    author_ids_for_new_paper = []

    for author_name in new_paper["authors"]:
        found_author_id = None

        # Check entity_keys first
        if "authors" in entity_keys:
            for a_id, a_info in entity_keys["authors"].items():
                if (
                    a_info.get("name") == author_name
                    or a_info.get("raw_name") == author_name
                ):
                    found_author_id = a_id
                    break

        # If not found in entity_keys, check authors
        if not found_author_id:
            for author_obj in authors:
                if (
                    author_obj["raw_name"] == author_name
                    or author_obj["standardized_name"] == author_name
                ):
                    found_author_id = author_obj["id"]
                    break

        # If still not found, create a new author entry
        if not found_author_id:
            new_id = f"author-{len(authors) + 100}"  # ID generation logic
            found_author_id = new_id

            new_author_obj = {
                "id": new_id,
                "raw_name": author_name,
                "standardized_name": author_name,
                "openalex_link": None,
                "orcid": None,
                "citation": [],
                "venue": [],
                "author_graph": [],
            }
            authors.append(new_author_obj)

            # Also update entity_keys
            if (
                "authors" not in entity_keys
            ):  # this should never happen, another point for needing to actually type everything
                entity_keys["authors"] = {}

            entity_keys["authors"][new_id] = {
                "name": author_name,
                "s2_id": None,
                "orcid": None,
                "raw_name": author_name,
            }

        author_ids_for_new_paper.append(found_author_id)

    # --- 4) Identify existing hop-1 citations to list in citation_graph --- #
    hop1_citation_ids = []
    for citation_key, c in citations.items():
        if c["hop"] == 1:
            hop1_citation_ids.append(citation_key)

    # --- 5) Create the new citation entry (hop=0) --- #
    new_citation_entry = {
        "citation_key": new_citation_id,
        "cite_number": 0,
        "authors": author_ids_for_new_paper,
        "venue": "venue-??",  # or update with a real venue ID if you have one
        "year": new_paper["year"],
        "title": new_paper["title"],
        "source": (
            f"{', '.join(new_paper['authors'])}. "
            f'"{new_paper["title"]}", ???, {new_paper["year"]}.'
        ),
        "hop": 0,
        "citation_graph": hop1_citation_ids,
    }

    # Append this new citation
    citations[new_citation_id] = new_citation_entry

    coauthor_ids = set(author_ids_for_new_paper)
    # could this have been done above?
    for a_id in author_ids_for_new_paper:
        for a_obj in authors:
            if a_obj["id"] == a_id:
                if new_citation_id not in a_obj["citation"]:
                    a_obj["citation"].append(new_citation_id)
                # Add coauthors to author_graph
                for other_id in coauthor_ids:
                    if other_id != a_id and other_id not in a_obj["author_graph"]:
                        a_obj["author_graph"].append(other_id)
                break

    return citations, authors, venues


# not used?
def build_author_graph(citations):
    # 2. Build a dictionary mapping citation_id -> list of authors
    citation_to_authors = {}
    for citation_id, c in citations.items():
        citation_authors = c["authors"]  # e.g. ["author-1", "author-2", ...]
        citation_to_authors[citation_id] = citation_authors

    # 3. Initialize a counter for (citing_author -> cited_author) edges
    author_citation_counter = defaultdict(int)

    # 4. Traverse each citation's citation_graph
    for c in citations.values():
        citing_authors = c["authors"]
        # 'citation_graph' is a list of cited citation IDs
        # don't need the citation_graph object, can just look at references and get keys from there
        citation_graph = [
            x.get("citation_key", "") for x in c.get("enriched_references", [])
        ]
        for cited_citation_id in citation_graph:
            # Find the authors of the cited paper
            cited_authors = citation_to_authors.get(cited_citation_id, [])
            # Increment the counter for each pair (citing_author, cited_author)
            for a_citing in citing_authors:
                for a_cited in cited_authors:
                    author_citation_counter[(a_citing, a_cited)] += 1

    # 5. Convert the counter dictionary to the desired list-of-dicts format
    edges = []
    for (author_src, author_tgt), count in author_citation_counter.items():
        edges.append({"source": author_src, "target": author_tgt, "value": count})

    # Sort edges by descending 'value' if you wish (optional)
    edges.sort(key=lambda x: x["value"], reverse=True)

    return edges
