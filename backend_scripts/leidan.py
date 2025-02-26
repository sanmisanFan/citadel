import json
import igraph as ig
import leidenalg as la
import matplotlib.pyplot as plt  # for igraph's plotting

# --- Load JSON data ---
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
    
    # 2) Citation: directed from citing → cited
    for cited_id in cited_ids:
        cited_authors = next(c['author'] for c in citations_data if c['id'] == cited_id)
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
        pass

# Add edges to the graph
author_G.add_edges(edge_list)

# ----------------------------------------------------------------------
#  1) Run the Leiden algorithm
# ----------------------------------------------------------------------
# Leiden can be used with various VertexPartition classes, each measuring
# “community quality” differently. For directed graphs, you can use
# RBConfigurationVertexPartition (or alternatives like CPMVertexPartition).
# If your edges have weights, provide 'weights' in the call.

partition = la.find_partition(
    author_G,
    la.RBConfigurationVertexPartition,  # Works on directed graphs
    weights=None,                       # or 'weight' if you tracked weights
    resolution_parameter=1.0
)

# partition.membership is a list, where each element is the community ID
# for the corresponding node (vertex)

# ----------------------------------------------------------------------
#  2) Examine Communities
# ----------------------------------------------------------------------
communities = {}
for i, comm_id in enumerate(partition.membership):
    communities.setdefault(comm_id, []).append(author_G.vs[i]['name'])

for comm_id, member_list in communities.items():
    print(f"Community {comm_id} (size={len(member_list)}):")
    for name in member_list:
        print("   ", name)

# If you want to measure the modularity-like score for this partition:
print("\nPartition quality (modularity-like):", partition.quality())

# ----------------------------------------------------------------------
#  3) Plot the Graph with Community Colors
# ----------------------------------------------------------------------
# Assign each community a color
colors = [
    "red", "blue", "green", "yellow", "purple", "orange",
    "pink", "cyan", "magenta", "lime"
]
for v_idx, comm_id in enumerate(partition.membership):
    author_G.vs[v_idx]["color"] = colors[comm_id % len(colors)]

# Layout and style
layout = author_G.layout("kk")  # or "fr", "graphopt", etc.
visual_style = {
    "layout": layout,
    "vertex_size": 20,
    "vertex_label": author_G.vs['name'],
    "vertex_label_size": 10,
    "edge_arrow_size": 0.8,
    "edge_curved": 0.2,
    "bbox": (2000, 2000),
    "margin": 100
}

try:
    ig.plot(author_G, target="directed_leiden_graph.png", **visual_style)
    print("Graph with Leiden communities saved as 'directed_leiden_graph.png'")
except AttributeError as e:
    print(f"Plotting failed: {e}\nPlease ensure pycairo or cairocffi is installed.")
