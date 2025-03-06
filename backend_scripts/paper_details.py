import json
from pathlib import Path

# --- 1) Read existing data --- #
authors_path = Path("./outputs/authors.json")
citations_path = Path("./outputs/citations.json")
venues_path = Path("./outputs/venues.json")
entity_keys_path = Path("./outputs/entity_keys.json")

with authors_path.open("r", encoding="utf-8") as f:
    authors_data = json.load(f)

with citations_path.open("r", encoding="utf-8") as f:
    citations_data = json.load(f)

with venues_path.open("r", encoding="utf-8") as f:
    venues_data = json.load(f)

with entity_keys_path.open("r", encoding="utf-8") as f:
    entity_keys_data = json.load(f)

# --- 2) Your new paper info --- #
new_paper = {
    "title": "A Demo Manuscript as a ReviewerApp Study Case",
    "authors": ["Han Solo", "Luke Skywalker", "Obi-Wan Kenobi"],
    "year": 2025
}
new_citation_id = "citation-0"

# --- 3) Find or create each author ID from the new paper --- #
author_ids_for_new_paper = []

for author_name in new_paper["authors"]:
    found_author_id = None
    
    # Check entity_keys first
    if "authors" in entity_keys_data:
        for a_id, a_info in entity_keys_data["authors"].items():
            # Compare by 'name' or 'raw_name'
            if a_info.get("name") == author_name or a_info.get("raw_name") == author_name:
                found_author_id = a_id
                break

    # If not found in entity_keys, check authors_data
    if not found_author_id:
        for author_obj in authors_data["authors"]:
            if (author_obj["raw_name"] == author_name 
                or author_obj["standardized_name"] == author_name):
                found_author_id = author_obj["id"]
                break

    # If still not found, create a new author entry
    if not found_author_id:
        new_id = f"author-{len(authors_data['authors'])+100}"  # ID generation logic
        found_author_id = new_id
        
        new_author_obj = {
            "id": new_id,
            "raw_name": author_name,
            "standardized_name": author_name,
            "openalex_link": None,
            "orcid": None,
            "citation": [],
            "venue": [],
            "author_graph": []
        }
        authors_data["authors"].append(new_author_obj)
        
        # Also update entity_keys
        if "authors" not in entity_keys_data:
            entity_keys_data["authors"] = {}
        entity_keys_data["authors"][new_id] = {
            "name": author_name,
            "s2_id": None,
            "orcid": None,
            "raw_name": author_name
        }

    author_ids_for_new_paper.append(found_author_id)

# --- 4) Identify existing hop-1 citations to list in citation_graph --- #
hop1_citation_ids = []
for c in citations_data["citations"]:
    if c["hop"] == 1:
        hop1_citation_ids.append(c["id"])

# --- 5) Create the new citation entry (hop=0) --- #
new_citation_entry = {
    "id": new_citation_id,
    "cite_number": 0,
    "author": author_ids_for_new_paper,
    "venue": "venue-??",  # or update with a real venue ID if you have one
    "year": new_paper["year"],
    "title": new_paper["title"],
    "source": (
       f"{', '.join(new_paper['authors'])}. "
       f"\"{new_paper['title']}\", ???, {new_paper['year']}."
    ),
    "hop": 0,
    "cite_positions": [],
    "has_issue": False,
    "citation_graph": hop1_citation_ids
}

# Append this new citation
citations_data["citations"].append(new_citation_entry)

# --- 6) Update each author’s "citation" array and "author_graph" --- #
coauthor_ids = set(author_ids_for_new_paper)

for a_id in author_ids_for_new_paper:
    for a_obj in authors_data["authors"]:
        if a_obj["id"] == a_id:
            if new_citation_id not in a_obj["citation"]:
                a_obj["citation"].append(new_citation_id)
            # Add coauthors to author_graph
            for other_id in coauthor_ids:
                if other_id != a_id and other_id not in a_obj["author_graph"]:
                    a_obj["author_graph"].append(other_id)
            break

print("New paper added as citation-0 with hop=0, authors updated!")

# ---------------------------------------------------------------------
# Option A: Write each updated data structure to its own NEW JSON file:
# ---------------------------------------------------------------------
authors_output_path = Path("./outputs/authors_updated.json")
citations_output_path = Path("./outputs/citations_updated.json")
venues_output_path = Path("./outputs/venues_updated.json")
entity_keys_output_path = Path("./outputs/entity_keys_updated.json")

with authors_output_path.open("w", encoding="utf-8") as f:
    json.dump(authors_data, f, indent=2)

with citations_output_path.open("w", encoding="utf-8") as f:
    json.dump(citations_data, f, indent=2)

with venues_output_path.open("w", encoding="utf-8") as f:
    json.dump(venues_data, f, indent=2)

with entity_keys_output_path.open("w", encoding="utf-8") as f:
    json.dump(entity_keys_data, f, indent=2)


