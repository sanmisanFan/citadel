import json
import random

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_authors_from_paper(paper, authors_dict):
    """
    Update authors_dict with author information extracted from a paper.
    'paper' is expected to have a key "authors", a list of author dictionaries.
    Each author dictionary may contain:
      - "s2_id": Semantic Scholar ID
      - "raw_name": the original name
      - "name": the standardized name
      - "orcid": ORCID link (optional)
    Also, each paper is expected to have a unique identifier,
    which we add to the "citation" set and the "venue" set.
    """
    venue = paper.get("venue", "")
    paper_id = paper.get("semantic_scholar_id", "") or paper.get("doi", "")
    for author in paper.get("authors", []):
        if author is None:
            continue
        # Use s2_id if available; otherwise, use raw_name
        key = author.get("s2_id")
        if not key:
            raw_name = author.get("raw_name", "")
            key = raw_name.strip() if raw_name else None
            if not key:
                continue
        if key not in authors_dict:
            authors_dict[key] = {
                "raw_name": author.get("raw_name", author.get("name", "")),
                "standardized_name": author.get("name", author.get("raw_name", "")),
                "openalex_link": author.get("openalex_link", ""),  # if available
                "orcid": author.get("orcid") if author.get("orcid") is not None else "",
                "citation": set(),  # using a set to avoid duplicates
                "venue": set(),     # using a set to avoid duplicates
                "author_graph": []  # placeholder for later population
            }
        if paper_id:
            authors_dict[key]["citation"].add(paper_id)
        if venue:
            authors_dict[key]["venue"].add(venue)

def process_authors(enriched_papers, enriched_second_hop):
    """
    Process both first-hop and second-hop data to build a unified list of author objects.
    Each author is assigned a sequential id ("author-0", "author-1", ...).
    """
    authors_dict = {}
    
    # Process first-hop enriched papers.
    for paper in enriched_papers:
        merge_authors_from_paper(paper, authors_dict)
    
    # Process second-hop enriched data.
    # Assumes enriched_second_hop is a dict keyed by first-hop paper IDs, each with a "references" list.
    for first_hop_id, paper_data in enriched_second_hop.items():
        for ref in paper_data.get("references", []):
            merge_authors_from_paper(ref, authors_dict)
    
    # Convert the dictionary into a list of author objects with sequential IDs.
    author_objects = []
    for i, (key, data) in enumerate(authors_dict.items()):
        # Process ORCID field: if it contains "orcid.org/", keep only the raw id.
        orcid_val = data["orcid"]
        if isinstance(orcid_val, str) and "orcid.org/" in orcid_val:
            orcid_val = orcid_val.split("orcid.org/")[-1]
        author_obj = {
            "id": f"author-{i}",
            "raw_name": data["raw_name"],
            "standardized_name": data["standardized_name"],
            "openalex_link": data["openalex_link"],
            "orcid": orcid_val,
            "citation": list(data["citation"]),
            "venue": list(data["venue"]),
            "author_graph": data["author_graph"]
        }
        author_objects.append(author_obj)
    
    return {"authors": author_objects}

def assign_external_keys(authors_data):
    """
    Build two mapping dictionaries:
      - citation_mapping: maps each original citation value (paper id) to a new key "citation-<n>"
      - venue_mapping: maps each unique venue string to a new random unique key "venue-<num>"
    Then update each author object so that their citation and venue lists contain these new keys.
    Returns the combined mapping in a dictionary with keys "citation" and "venue".
    """
    citation_mapping = {}
    venue_mapping = {}
    next_citation_index = 0
    used_venue_numbers = set()
    
    # Collect unique citation and venue values from all authors.
    for author in authors_data.get("authors", []):
        for cit in author.get("citation", []):
            if cit not in citation_mapping:
                citation_mapping[cit] = f"citation-{next_citation_index}"
                next_citation_index += 1
        for ven in author.get("venue", []):
            if ven not in venue_mapping:
                # Generate a random number between 0 and 999 that hasn't been used.
                while True:
                    num = random.randint(0, 999)
                    if num not in used_venue_numbers:
                        used_venue_numbers.add(num)
                        break
                venue_mapping[ven] = f"venue-{num}"
    
    # Update author objects: replace citations and venues with the new keys.
    for author in authors_data.get("authors", []):
        author["citation"] = [citation_mapping[c] for c in author.get("citation", []) if c in citation_mapping]
        author["venue"] = [venue_mapping[v] for v in author.get("venue", []) if v in venue_mapping]
    
    return {"citation": citation_mapping, "venue": venue_mapping}

def main():
    # Load first-hop and second-hop enriched data.
    enriched_papers = load_json("enriched_papers.json")
    enriched_second_hop = load_json("second_hop_references.json")
    
    # Process authors from both datasets.
    authors_data = process_authors(enriched_papers, enriched_second_hop)
    
    # Assign new external keys for citations and venues and update the author objects.
    external_keys = assign_external_keys(authors_data)
    
    # Save the authors data.
    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, indent=2, ensure_ascii=False)
    
    # Save the external keys mapping.
    with open("external_keys.json", "w", encoding="utf-8") as f:
        json.dump(external_keys, f, indent=2, ensure_ascii=False)
    
    print("Author objects have been created and saved to authors.json")
    print("External keys have been created and saved to external_keys.json")

if __name__ == "__main__":
    main()
