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
    venue = paper.get("venue", "").strip()
    paper_id = paper.get("semantic_scholar_id", "") or paper.get("doi", "")
    for author in paper.get("authors", []):
        if author is None:
            continue
        # Use s2_id if available; otherwise, fallback to raw_name
        if isinstance(author, dict):
            key = author.get("s2_id")
            if not key:
                raw_name = author.get("raw_name") or ""
                key = raw_name.strip()
                if not key:
                    continue
        elif isinstance(author, str):
            key = author.strip()
        else:
            continue
        if key not in authors_dict:
            authors_dict[key] = {
                "raw_name": author.get("raw_name", author.get("name", "")) if isinstance(author, dict) else key,
                "standardized_name": author.get("name", author.get("raw_name", "")) if isinstance(author, dict) else key,
                "openalex_link": author.get("openalex_link", "") if isinstance(author, dict) else "",
                "orcid": author.get("orcid") if (isinstance(author, dict) and author.get("orcid") is not None) else "",
                "citation": set(),  # using a set to avoid duplicates
                "venue": set(),     # using a set to avoid duplicates
                "author_graph": []  # placeholder for later population
            }
        if paper_id:
            authors_dict[key]["citation"].add(paper_id)
        if venue:
            authors_dict[key]["venue"].add(venue)

def generate_venue_mapping(enriched_papers, enriched_second_hop):
    """
    Generate a mapping for venues from both first-hop and second-hop data.
    Returns a dictionary mapping each unique venue string to a key (e.g., "venue-0").
    """
    venue_set = set()
    
    def add_venue_from_paper(paper):
        venue = paper.get("venue", "").strip()
        if venue:
            venue_set.add(venue)
    
    for paper in enriched_papers:
        add_venue_from_paper(paper)
    
    for first_hop_id, paper_data in enriched_second_hop.items():
        for ref in paper_data.get("references", []):
            add_venue_from_paper(ref)
    
    mapping = {}
    for i, ven in enumerate(sorted(venue_set)):
        mapping[ven] = f"venue-{i}"
    return mapping

def process_authors(enriched_papers, enriched_second_hop, venue_mapping):
    """
    Process both first-hop and second-hop data to build a unified list of author objects.
    Each author is assigned a sequential id ("author-0", "author-1", ...).
    Also, update the author objects so that the "venue" list contains external keys from venue_mapping.
    """
    authors_dict = {}
    
    for paper in enriched_papers:
        merge_authors_from_paper(paper, authors_dict)
    
    for first_hop_id, paper_data in enriched_second_hop.items():
        for ref in paper_data.get("references", []):
            merge_authors_from_paper(ref, authors_dict)
    
    author_objects = []
    for i, (key, data) in enumerate(authors_dict.items()):
        orcid_val = data["orcid"]
        if isinstance(orcid_val, str) and "orcid.org/" in orcid_val:
            orcid_val = orcid_val.split("orcid.org/")[-1]
        venue_keys = [venue_mapping[v] for v in data["venue"] if v in venue_mapping]
        author_obj = {
            "id": f"author-{i}",
            "raw_name": data["raw_name"],
            "standardized_name": data["standardized_name"],
            "openalex_link": data["openalex_link"],
            "orcid": orcid_val,
            "citation": list(data["citation"]),
            "venue": venue_keys,
            "author_graph": data["author_graph"]
        }
        author_objects.append(author_obj)
    
    return {"authors": author_objects}

def process_venues(enriched_papers, enriched_second_hop, venue_mapping):
    """
    Process first-hop and second-hop data to build a list of venue objects.
    Use the shared venue_mapping to ensure consistency with the authors' venue keys.
    For each venue, collect all raw names, years, authors, and citations.
    """
    venues_dict = {}
    
    def add_paper_venue(paper):
        ven = paper.get("venue", "").strip()
        if not ven:
            return
        norm = ven.lower()
        if norm not in venues_dict:
            venues_dict[norm] = {
                "raw_names": set(),
                "years": set(),
                "authors": set(),
                "citations": set()
            }
        venues_dict[norm]["raw_names"].add(ven)
        year = paper.get("year")
        if year:
            venues_dict[norm]["years"].add(str(year))
        paper_id = paper.get("semantic_scholar_id", "") or paper.get("doi", "")
        if paper_id:
            venues_dict[norm]["citations"].add(paper_id)
        for author in paper.get("authors", []):
            if not author:
                continue
            if isinstance(author, dict):
                a_id = author.get("s2_id") or (author.get("raw_name") or "").strip()
            elif isinstance(author, str):
                a_id = author.strip()
            else:
                a_id = None
            if a_id:
                venues_dict[norm]["authors"].add(a_id)
    
    for paper in enriched_papers:
        add_paper_venue(paper)
    for first_hop_id, paper_data in enriched_second_hop.items():
        for ref in paper_data.get("references", []):
            add_paper_venue(ref)
    
    venue_objects = []
    for raw_venue, ext_key in venue_mapping.items():
        norm = raw_venue.lower()
        data = venues_dict.get(norm, {"raw_names": set(), "years": set(), "authors": set(), "citations": set()})
        raw_names_list = list(data["raw_names"]) if data["raw_names"] else [raw_venue]
        short_name = min(raw_names_list, key=len) if raw_names_list else raw_venue
        standardized_name = max(raw_names_list, key=len) if raw_names_list else raw_venue
        venue_obj = {
            "id": ext_key,
            "type": "Unknown",  # Adjust type as needed
            "raw_name": raw_names_list,
            "short": short_name,
            "standardized_name": standardized_name,
            "year": list(data["years"]),
            "author": list(data["authors"]),
            "citation": list(data["citations"]),
            "venue_graph": ["venue-graph-0"]  # Placeholder
        }
        venue_objects.append(venue_obj)
    
    return {"venues": venue_objects}

def main():
    enriched_papers = load_json("enriched_papers.json")
    enriched_second_hop = load_json("second_hop_references.json")
    
    venue_mapping = generate_venue_mapping(enriched_papers, enriched_second_hop)
    
    authors_data = process_authors(enriched_papers, enriched_second_hop, venue_mapping)
    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, indent=2, ensure_ascii=False)
    
    venues_data = process_venues(enriched_papers, enriched_second_hop, venue_mapping)
    with open("venues.json", "w", encoding="utf-8") as f:
        json.dump(venues_data, f, indent=2, ensure_ascii=False)
    
    external_keys = {"venue": venue_mapping}
    with open("external_keys.json", "w", encoding="utf-8") as f:
        json.dump(external_keys, f, indent=2, ensure_ascii=False)
    
    print("Author objects have been created and saved to authors.json")
    print("Venue objects have been created and saved to venues.json")
    print("External keys have been saved to external_keys.json")

if __name__ == "__main__":
    main()
