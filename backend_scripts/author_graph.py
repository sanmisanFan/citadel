import json
import igraph as ig
import matplotlib.pyplot as plt  # Required for igraph plotting backend

# --- Load the JSON data ---
with open('outputs/citations.json', 'r') as f:
    citations_data = json.load(f)['citations']

with open('outputs/authors.json', 'r') as f:
    authors_data = json.load(f)['authors']

# --- Create a directed graph ---
author_G = ig.Graph(directed=True)

# --- Add vertices (authors) ---
author_ids = [a['id'] for a in authors_data]
author_G.add_vertices(author_ids)
for i, author in enumerate(authors_data):
    author_G.vs[i]['name'] = author['standardized_name']

# --- Build edges ---
all_edges = []
for citation in citations_data:
    authors = citation['author']
    cited_ids = citation['citation_graph']
    
    # 1) Co-authorship: add both directions
    for i, a1 in enumerate(authors):
        for a2 in authors[i+1:]:
            all_edges.append((a1, a2))
            all_edges.append((a2, a1))
    
    # 2) Citations: directed from citing author to cited author
    for cited_id in cited_ids:
        # Find the corresponding entry to get its authors
        cited_authors = next(c['author'] for c in citations_data if c['id'] == cited_id)
        # For each citing author → each cited author
        for a1 in authors:
            for a2 in cited_authors:
                if a1 != a2:
                    all_edges.append((a1, a2))

# Remove duplicates, convert to graph indices
unique_edges = list(set(all_edges))
edge_list = []
for src, tgt in unique_edges:
    try:
        src_idx = author_ids.index(src)
        tgt_idx = author_ids.index(tgt)
        edge_list.append((src_idx, tgt_idx))
    except ValueError:
        # In case an ID wasn't found in author_ids
        pass

# Add edges to the graph
author_G.add_edges(edge_list)

# --- Layout & Plotting ---
# Try different layouts, e.g. "kk", "fr", or "graphopt"
layout = author_G.layout("graphopt")

# Large bounding box to reduce overlap
visual_style = {
    "layout": layout,
    "vertex_size": 20,
    "vertex_color": "skyblue",
    "vertex_label": [v["name"] for v in author_G.vs],
    "vertex_label_size": 10,
    "vertex_label_dist": 2,        # Push labels away from nodes
    "edge_curved": 0.2,           # Slight curve to edges
    "edge_arrow_size": 0.8,
    "edge_width": 1.0,
    "bbox": (2000, 2000),         # Large figure
    "margin": 100
}

# Plot to file
try:
    ig.plot(author_G, target="directed_author_graph.png", **visual_style)
    print("Directed graph saved as 'directed_author_graph.png'")
except AttributeError as e:
    print(f"Plotting failed: {e}\nPlease ensure pycairo or cairocffi is installed.")
