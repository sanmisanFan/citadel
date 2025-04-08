import json

# Load input JSON files with UTF-8 encoding
with open('outputs/enriched_papers_with_bboxes.json', 'r', encoding='utf-8') as f:
    enriched_papers = json.load(f)

with open('outputs/second_hop_references.json', 'r', encoding='utf-8') as f:
    second_hop = json.load(f)

with open('outputs/entity_keys.json', 'r', encoding='utf-8') as f:
    entity_keys = json.load(f)

# Step 1: Prepare hop 1 citation keys and ref_id mapping
hop1_citation_keys = set(paper["citation_key"] for paper in enriched_papers)
hop1_ref_id_dict = {paper["citation_key"]: paper["ref_id"] for paper in enriched_papers}
max_ref_id = max(hop1_ref_id_dict.values()) if hop1_ref_id_dict else 0

# Create a dictionary for hop 1 papers for easy access
hop1_papers_dict = {paper["citation_key"]: paper for paper in enriched_papers}

# Step 2: Build hop 1 to hop 2 citation graph mapping and title lookup
hop1_to_hop2 = {}
title_to_citation_key = {}  # Map titles to citation keys to detect duplicates

# Process hop 1 citations first
citations = []
seen_citation_keys = set()

for paper in enriched_papers:
    citation_key = paper["citation_key"]
    title = paper["title"].lower().strip()  # Normalize title for comparison
    cite_number = paper["ref_id"]
    cite_positions = []
    for mention in paper.get("reference_mentions", []):
        for cit in mention.get("citations", []):
            if cit["citation"] == f"[{cite_number}]":
                cite_positions.append({
                    "page": mention["page"],
                    "has_issue": False,
                    "issues": [],
                    "bbox": cit["bbox"]
                })

    citation_obj = {
        "id": citation_key,
        "cite_number": cite_number,
        "author": paper.get("authors", []),
        "venue": paper.get("venue", ""),
        "year": paper.get("year", None),
        "title": paper.get("title", ""),
        "source": f"{', '.join([str(entity_keys['authors'].get(a, {}).get('raw_name')) or str(entity_keys['authors'].get(a, {}).get('name')) or 'Unknown Author' for a in paper.get('authors', [])])}. \"{paper.get('title', 'Unknown Title')},\" {paper.get('raw_venue', 'Unknown Venue')}, {paper.get('year', 'Unknown Year')}.",
        "hop": 1,
        "cite_positions": cite_positions,
        "has_issue": False,
        "citation_graph": []  # To be populated later
    }
    citations.append(citation_obj)
    seen_citation_keys.add(citation_key)
    title_to_citation_key[title] = citation_key

    # Map hop 1 to hop 2 citations
    semantic_scholar_id = paper.get("semantic_scholar_id")
    if semantic_scholar_id in second_hop:
        hop2_refs = second_hop[semantic_scholar_id].get("references", [])
        hop1_to_hop2[citation_key] = []  # Initialize empty list, to be filled with unique hop 2 keys

# Step 3: Process hop 2 citations, checking for duplicates by title
hop2_counter = max_ref_id + 1

for paper_id, data in second_hop.items():
    hop1_citation_key = next((p["citation_key"] for p in enriched_papers if p.get("semantic_scholar_id") == paper_id), None)
    for ref in data.get("references", []):
        title = ref["title"].lower().strip() if ref.get("title") else "Unknown Title"
        existing_citation_key = title_to_citation_key.get(title)

        if existing_citation_key and existing_citation_key in hop1_citation_keys:
            # Duplicate title found in hop 1, link it to hop 1 citation
            if hop1_citation_key and existing_citation_key not in hop1_to_hop2[hop1_citation_key]:
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
                "source": f"{', '.join([entity_keys['authors'][a]['name'] for a in ref['authors'] if a in entity_keys['authors']])}. \"{ref['title']},\" {ref.get('venue', '')}, {ref.get('year', '')}.",
                "doi": ref.get("doi", None),
                "hop": 2,
                "cite_positions": [],
                "has_issue": False,
                "citation_graph": []
            }
            citations.append(citation_obj)
            seen_citation_keys.add(citation_key)
            title_to_citation_key[title] = citation_key
            hop2_counter += 1

        # Link hop 2 citation to its hop 1 parent
        if hop1_citation_key and citation_key not in hop1_to_hop2[hop1_citation_key]:
            hop1_to_hop2[hop1_citation_key].append(citation_key)

# Step 4: Update citation_graph in all citations
for citation in citations:
    citation["citation_graph"] = hop1_to_hop2.get(citation["id"], [])

# Step 5: Update entity_keys["citations"] with all citations
for citation in citations:
    if citation["id"] not in entity_keys["citations"]:
        entity_keys["citations"][citation["id"]] = {
            "title": citation["title"],
            "authors": citation["author"],
            "venue": citation["venue"],
            "year": citation["year"],
            "doi": citation["doi"],
            "raw_venue": hop1_papers_dict.get(citation["id"], {}).get("raw_venue", citation["venue"])
        }

# Step 6: Create author_citations and author_venues mappings
author_citations = {}
author_venues = {}
for citation in citations:
    for author_id in citation["author"]:
        if author_id not in author_citations:
            author_citations[author_id] = []
        author_citations[author_id].append(citation["id"])
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
        "author_graph": []
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
        "standardized_name": standardized_name
    }

for citation in citations:
    venue_id = citation["venue"]
    if venue_id and venue_id in venue_data:
        paper = entity_keys["citations"][citation["id"]]
        raw_venue = paper.get("raw_venue", "")
        if raw_venue:
            venue_data[venue_id]["raw_name"].add(raw_venue)
        if citation["year"]:
            venue_data[venue_id]["year"].add(str(citation["year"]))
        for author_id in citation["author"]:
            venue_data[venue_id]["author"].add(author_id)
        venue_data[venue_id]["citation"].add(citation["id"])

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
        "short": data["standardized_name"][:10] if data["standardized_name"] else "Unknown",
        "standardized_name": data["standardized_name"],
        "year": data["year"],
        "author": data["author"],
        "citation": data["citation"],
        "venue_graph": []
    }
    venues.append(venue_obj)

# Step 10: Save to JSON files with UTF-8 encoding
with open('outputs/citations.json', 'w', encoding='utf-8') as f:
    json.dump({"citations": citations}, f, indent=2)

with open('outputs/authors.json', 'w', encoding='utf-8') as f:
    json.dump({"authors": authors}, f, indent=2)

with open('outputs/venues.json', 'w', encoding='utf-8') as f:
    json.dump({"venues": venues}, f, indent=2)

print("JSON files generated: citations.json, authors.json, venues.json")