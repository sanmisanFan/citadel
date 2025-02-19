import json

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_citation_object(generated_id, cite_number, paper_data, hop, source_text=""):
    """
    Create a citation object from paper data.
    paper_data is expected to be a dictionary containing keys like:
      title, authors (list of dicts with keys: s2_id, raw_name, etc.), venue, year, doi, source,
      and optionally semantic_scholar_id.
    hop: integer (1 for first hop, 2 for second hop).
    source_text: if available, the original reference string.
    
    The citation object's id is taken from paper_data's "semantic_scholar_id" if available,
    otherwise it uses the provided generated_id.
    """
    # Use semantic_scholar_id if available; otherwise, use the generated id.
    citation_id = paper_data.get("semantic_scholar_id", generated_id)
    
    # Create a list of author keys using the s2_id if available; otherwise use a sanitized raw_name.
    author_keys = []
    for author in paper_data.get("authors", []):
        if not author:
            continue  # Skip if the author entry is None
        if author.get("s2_id"):
            author_keys.append(author["s2_id"])
        else:
            raw = author.get("raw_name", "")
            if raw:
                author_keys.append(raw.replace(" ", "_"))
    
    # For venue, use the venue string directly (or transform it if you have a mapping).
    venue_key = paper_data.get("venue", "unknown")
    
    citation_obj = {
        "id": citation_id,                   # Unique citation ID: uses Semantic Scholar id if available.
        "cite_number": cite_number,          # Sequential citation number
        "author": author_keys,               # List of author external keys
        "venue": venue_key,                  # Venue external key or name
        "year": paper_data.get("year"),      # Publication year (int)
        "title": paper_data.get("title"),    # Paper title (string)
        "source": source_text if source_text else paper_data.get("source", ""),  # Original reference text if available
        "doi": paper_data.get("doi", ""),    # DOI link (string)
        "hop": hop,                          # Hop level: 1 for first hop, 2 for second hop
        "cite_positions": [],                # Bounding-box data (empty list by default)
        "has_issue": False,                  # Set to false by default (can be updated later)
        "citation_graph": []                 # Citation graph keys (empty list by default)
    }
    return citation_obj

def main():
    # Load first-hop enriched papers and second-hop references
    enriched_papers = load_json("enriched_papers.json")         # Contains hop-1 paper details
    second_hop = load_json("second_hop_references.json")          # Contains a dict keyed by first-hop paper id
    
    citations = []
    citation_counter = 1

    # Process hop-1 citations (papers from the reference section of the reviewing paper)
    for paper in enriched_papers:
        gen_id = f"citation-{citation_counter}"
        citation_obj = create_citation_object(gen_id, citation_counter, paper, hop=1, 
                                                source_text=paper.get("source", ""))
        citations.append(citation_obj)
        citation_counter += 1

    # Process hop-2 citations (references from the hop-1 papers)
    for first_hop_id, ref_data in second_hop.items():
        for ref in ref_data.get("references", []):
            gen_id = f"citation-{citation_counter}"
            citation_obj = create_citation_object(gen_id, citation_counter, ref, hop=2, 
                                                    source_text=ref.get("source", ""))
            citations.append(citation_obj)
            citation_counter += 1

    # Wrap the citations into the final JSON object.
    output_data = {
        "citations": citations
    }

    # Save the output to a JSON file.
    with open("citations_object.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("Citation objects have been created and saved to citations_object.json")

if __name__ == "__main__":
    main()
