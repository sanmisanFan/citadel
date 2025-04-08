import json
from collections import defaultdict

def build_author_graph(citations_file_path, output_file_path=None):
    """
    Reads the citations JSON, builds a directed author-citation graph,
    and returns or saves a list of { "source", "target", "value" } edges.
    """

    # 1. Load citations JSON
    with open(citations_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        citations = data["citations"]

    # 2. Build a dictionary mapping citation_id -> list of authors
    citation_to_authors = {}
    for c in citations:
        citation_id = c["id"]
        citation_authors = c["author"]  # e.g. ["author-1", "author-2", ...]
        citation_to_authors[citation_id] = citation_authors

    # 3. Initialize a counter for (citing_author -> cited_author) edges
    author_citation_counter = defaultdict(int)

    # 4. Traverse each citation's citation_graph
    for c in citations:
        citing_authors = c["author"]
        # 'citation_graph' is a list of cited citation IDs
        for cited_citation_id in c.get("citation_graph", []):
            # Find the authors of the cited paper
            cited_authors = citation_to_authors.get(cited_citation_id, [])
            # Increment the counter for each pair (citing_author, cited_author)
            for a_citing in citing_authors:
                for a_cited in cited_authors:
                    author_citation_counter[(a_citing, a_cited)] += 1

    # 5. Convert the counter dictionary to the desired list-of-dicts format
    edges = []
    for (author_src, author_tgt), count in author_citation_counter.items():
        edges.append({
            "source": author_src,
            "target": author_tgt,
            "value": count
        })

    # Sort edges by descending 'value' if you wish (optional)
    edges.sort(key=lambda x: x["value"], reverse=True)

    # Optionally save to file
    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as out_f:
            json.dump(edges, out_f, indent=2)

    return edges

if __name__ == "__main__":
    # Example usage
    # Adjust the file paths as needed
    input_citations = "./outputs/citations_updated.json"
    output_edges = "./outputs/author_graph.json"

    author_edges = build_author_graph(input_citations, output_edges)
    print("Number of edges:", len(author_edges))
    # Uncomment below to preview some edges in console
    # for e in author_edges[:10]:
    #     print(e)
