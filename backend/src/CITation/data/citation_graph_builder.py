import json
from .datatypes import PaperMetadata


def extract_info(enriched_papers, entity_keys, new_paper: PaperMetadata):
    # Step 1: Prepare hop 1 citation keys and ref_id mapping
    print(enriched_papers)
    hop1_ref_id_dict = {
        paper["citation_key"]: paper["ref_id"] for paper in enriched_papers.values()
    }
    # max_ref_id = max(hop1_ref_id_dict.values()) if hop1_ref_id_dict else 0
    # Create a dictionary for hop 1 papers for easy access
    # hop1_papers_dict = {paper["citation_key"]: paper for paper in enriched_papers}

    # Step 2: Build hop 1 to hop 2 citation graph mapping and title lookup
    # hop1_to_hop2 = {}
    # title_to_citation_key = {}  # Map titles to citation keys to detect duplicates

    # Process hop 1 citations first
    # pretty sure we can just read entity_keys['citations'] and be done here...
    citations = entity_keys["citations"]
    # seen_citation_keys = set()

    # https://github.com/sanmisanFan/research_reviewer_main/blob/main/Documents/API_instruction.md
    """
    for paper in enriched_papers:
        citation_key = paper["citation_key"]
        title = paper["title"].lower().strip()  # Normalize title for comparison
        cite_number = paper["ref_id"]
        we don't have this information at the moment
        cite_positions = []
        for mention in paper.get("reference_mentions", []):
            for cit in mention.get("citations", []):
                if cit["citation"] == f"[{cite_number}]":
                    cite_positions.append(
                        {
                            "page": mention["page"],
                            "has_issue": False,
                            "issues": [],
                            "bbox": cit["bbox"],
                        }
                    )
        # this just copies the info from enriched papers and doesn't really add anything
        citation_obj = {
            "id": citation_key,
            "cite_number": cite_number,
            "author": paper.get("authors", []),
            "venue": paper.get("venue", ""),
            "year": paper.get("year", None),
            "title": paper.get("title", ""),
            "source": f'{", ".join([str(entity_keys["authors"].get(a, {}).get("raw_name")) or str(entity_keys["authors"].get(a, {}).get("name")) or "Unknown Author" for a in paper.get("authors", [])])}. "{paper.get("title", "Unknown Title")}," {paper.get("raw_venue", "Unknown Venue")}, {paper.get("year", "Unknown Year")}.',
            "hop": 1,
            "doi": paper.get("doi", "https://google.com"),
            "has_issue": False,
            "citation_graph": [],  # To be populated later
        }
        citations.append(citation_obj)
        seen_citation_keys.add(citation_key)
        title_to_citation_key[title] = citation_key

        # Map hop 1 to hop 2 citations
        semantic_scholar_id = paper.get("semantic_scholar_id")
        if semantic_scholar_id in second_hop:
            hop1_to_hop2[
                citation_key
            ] = []  # Initialize empty list, to be filled with unique hop 2 keys

    # Step 3: Process hop 2 citations, checking for duplicates by title
    hop2_counter = max_ref_id + 1
    # this seems to be pointless, the data is already available in the entity_keys json
    for paper_id, data in second_hop.items():
        hop1_citation_key = next(
            (
                p["citation_key"]
                for p in enriched_papers
                if p.get("semantic_scholar_id") == paper_id
            ),
            None,
        )
        # why are we looking at the references for the second hop references?
        for ref in data.get("references", []):
            title = (
                ref["title"].lower().strip() if ref.get("title") else "Unknown Title"
            )
            existing_citation_key = title_to_citation_key.get(title)

            if existing_citation_key and existing_citation_key in hop1_citation_keys:
                # Duplicate title found in hop 1, link it to hop 1 citation
                if (
                    hop1_citation_key
                    and existing_citation_key not in hop1_to_hop2[hop1_citation_key]
                ):
                    hop1_to_hop2[hop1_citation_key].append(existing_citation_key)
                continue  # Skip adding a new citation object

            citation_key = ref["citation_key"]
            if citation_key not in seen_citation_keys:
                citation_obj = {
                    "id": citation_key,
                    "cite_number": hop2_counter,
                    "author": ref.get("authors", []),
                    "venue": ref.get("venue", ""),
                    "year": ref.get("year", None),
                    "title": ref.get("title", ""),
                    "source": f'{", ".join([entity_keys["authors"][a]["name"] for a in ref["authors"] if a in entity_keys["authors"]])}. "{ref["title"]}," {ref.get("venue", "")}, {ref.get("year", "")}.',
                    "doi": ref.get("doi", None),
                    "hop": 2,
                    "cite_positions": [],
                    "has_issue": False,
                    "citation_graph": [],
                }
                citations.append(citation_obj)
                seen_citation_keys.add(citation_key)
                title_to_citation_key[title] = citation_key
                hop2_counter += 1

            # Link hop 2 citation to its hop 1 parent
            if (
                hop1_citation_key
                and citation_key not in hop1_to_hop2[hop1_citation_key]
            ):
                hop1_to_hop2[hop1_citation_key].append(citation_key)
    """

    # Step 4: Update citation_graph in all citations
    # we also should have this data in the entity_keys (through enriched_references)
    # for citation in citations:
    #    citation["citation_graph"] = hop1_to_hop2.get(citation["id"], [])

    # Step 5: Update entity_keys["citations"] with all citations
    """
    for citation in citations:
        if citation["id"] not in entity_keys["citations"]:
            entity_keys["citations"][citation["id"]] = {
                "title": citation["title"],
                "authors": citation["author"],
                "venue": citation["venue"],
                "year": citation["year"],
                "doi": citation["doi"],
                "raw_venue": hop1_papers_dict.get(citation["id"], {}).get(
                    "raw_venue", citation["venue"]
                ),
            }
    """

    # Step 6: Create author_citations and author_venues mappings
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

    # Step 7: Create author objects
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

    # Step 8: Create venue_data mappings
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

    # Convert sets to lists
    for venue_id in venue_data:
        venue_data[venue_id]["raw_name"] = list(venue_data[venue_id]["raw_name"])
        venue_data[venue_id]["year"] = list(venue_data[venue_id]["year"])
        venue_data[venue_id]["author"] = list(venue_data[venue_id]["author"])
        venue_data[venue_id]["citation"] = list(venue_data[venue_id]["citation"])

    # Step 9: Create venue objects
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
        "author": author_ids_for_new_paper,
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
