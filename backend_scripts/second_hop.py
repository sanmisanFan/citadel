import json
import requests

def get_paper_details(paper_id):
    """
    Fetch a paper's metadata including references, authors, and venue.
    paper_id: Can be a Semantic Scholar ID, DOI, or arXiv ID.
    Returns: JSON with paper details or None.
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/"
    fields = "title,authors,venue,year,references.title,references.authors,references.venue,references.year"
    
    try:
        response = requests.get(
            f"{base_url}{paper_id}",
            params={"fields": fields},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error for paper_id {paper_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"API request failed for paper_id {paper_id}: {e}")
        return None

def search_paper_by_title(title):
    """
    Search for a paper by its title using the Semantic Scholar search API
    and return the paper ID from the first result.
    """
    search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "paperId"
    }
    try:
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            results = response.json()
            if results.get("data") and len(results["data"]) > 0:
                first_result = results["data"][0]
                return first_result.get("paperId")
            else:
                print(f"No search results found for title: {title}")
                return None
        else:
            print(f"Search error for title '{title}': {response.status_code}")
            return None
    except Exception as e:
        print(f"Search request failed for title '{title}': {e}")
        return None

def process_papers(input_filename, output_filename):
    # Load the list of papers from the input JSON file.
    with open(input_filename, 'r', encoding='utf-8') as infile:
        papers = json.load(infile)
    
    processed_papers = []
    
    # Iterate over each paper in the list.
    for paper in papers:
        # Use DOI if available; otherwise, search by title.
        paper_id = paper.get("doi")
        if not paper_id:
            print(f"Paper '{paper.get('title', 'Unknown Title')}' lacks a DOI. Searching by title...")
            paper_id = search_paper_by_title(paper.get("title"))
            if not paper_id:
                print(f"Skipping paper '{paper.get('title', 'Unknown Title')}' due to missing DOI and failed title search.")
                continue
        
        # Fetch detailed information from the Semantic Scholar API.
        details = get_paper_details(paper_id)
        if details is None:
            print(f"Details not found for paper_id {paper_id}.")
            continue
        
        # Extract the desired details.
        paper_info = {
            "title": details.get("title"),
            "venue": details.get("venue"),
            "year": details.get("year"),
            "authors": [
                {"name": author.get("name"), "s2_id": author.get("authorId")}
                for author in details.get("authors", [])
            ],
            "references": []
        }
        
        # Process each reference.
        for ref in details.get("references", []):
            ref_info = {
                "title": ref.get("title"),
                "venue": ref.get("venue", "N/A"),
                "year": ref.get("year"),
                "authors": [a.get("name") for a in ref.get("authors", [])]
            }
            paper_info["references"].append(ref_info)
        
        processed_papers.append(paper_info)
    
    # Save the processed details to an output JSON file.
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(processed_papers, outfile, indent=4)
    
    print(f"Processed details for {len(processed_papers)} papers written to '{output_filename}'.")

if __name__ == "__main__":
    # Specify your input file (list of papers) and the output file.
    input_filename = "output.json"       # Adjust if your file name is different.
    output_filename = "hop2.json"
    process_papers(input_filename, output_filename)
