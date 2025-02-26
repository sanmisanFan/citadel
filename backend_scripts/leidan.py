import json
import igraph as ig
import leidenalg as la
import matplotlib.pyplot as plt  # Required for igraph plotting backend

# Load citations.json
with open('outputs/citations.json', 'r') as f:
    citations_data = json.load(f)['citations']

# Load authors.json
with open('outputs/authors.json', 'r') as f:
    authors_data = json.load(f)['authors']

# Create an undirected graph
author_G = ig.Graph(directed=False)

# Add vertices (authors)
author_ids = [a['id'] for a in authors_data]
author_G.add_vertices(author_ids)
for i, author in enumerate(authors_data):
    author_G.vs[i]['name'] = author['standardized_name']

# Add edges (co-authorship and citation links)
edges = {}
for citation in citations_data:
    authors = citation['author']
    cited_ids = citation['citation_graph']
    # Co-authorship
    for i, a1 in enumerate(authors):
        for a2 in authors[i+1:]:
            edge = tuple(sorted([a1, a2]))
            edges[edge] = edges.get(edge, 0) + 1
    # Citation links
    for cited_id in cited_ids:
        cited_authors = next(c['author'] for c in citations_data if c['id'] == cited_id)
        for a1 in authors:
            for a2 in cited_authors:
                if a1 != a2:
                    edge = tuple(sorted([a1, a2]))
                    edges[edge] = edges.get(edge, 0) + 1

# Add weighted edges
edge_list = [(author_ids.index(e[0]), author_ids.index(e[1])) for e in edges.keys()]
weight_list = [edges[e] for e in edges.keys()]
author_G.add_edges(edge_list)
author_G.es['weight'] = weight_list

print(author_G.summary())  # Check: nodes = authors, edges = relationships

# Apply Leiden with weighted modularity
partition = la.find_partition(author_G, la.ModularityVertexPartition, weights='weight')

# Extract communities
communities = {}
for i, vertex in enumerate(author_G.vs):
    comm_id = partition.membership[i]
    if comm_id not in communities:
        communities[comm_id] = []
    communities[comm_id].append(vertex['name'])

# Filter and display potential author rings
for comm_id, authors in communities.items():
    if len(authors) > 2:  # Filter small groups
        print(f"Author Community {comm_id} (Size: {len(authors)}):")
        for auth_name in authors:
            author = next(a for a in authors_data if a['standardized_name'] == auth_name)
            print(f" - {auth_name}: {author['citation']}")

# --- Improved Visualization ---
# Assign colors to communities
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'lime']
for i, vertex in enumerate(author_G.vs):
    comm_id = partition.membership[i]
    vertex['color'] = colors[comm_id % len(colors)]  # Cycle through colors

# Set node sizes based on degree (scaled down for clarity)
author_G.vs['size'] = [max(v.degree(), 1) * 5 + 10 for v in author_G.vs]  # Smaller nodes to reduce overlap

# Set labels (shortened to initials or first 10 characters)
author_G.vs['label'] = [name.split('.')[0][:10] + '...' if '.' in name else name[:10] + '...' for name in author_G.vs['name']]

# Use Kamada-Kawai layout for better spacing (or try "circle" for circular layout)
layout = author_G.layout("kk")  # Kamada-Kawai for clearer separation

# Filter to show only communities with >2 authors to reduce clutter
visible_nodes = []
for comm_id, authors in communities.items():
    if len(authors) > 2:
        for author in authors:
            idx = author_G.vs.find(name=author).index
            visible_nodes.append(idx)

# Subgraph with only selected nodes (and their edges)
subgraph = author_G.subgraph(visible_nodes)

# Visual style for the subgraph
visual_style = {
    "vertex_size": [max(v.degree(), 1) * 5 + 10 for v in subgraph.vs],  # Smaller nodes
    "vertex_color": [subgraph.vs[i]['color'] for i in range(len(subgraph.vs))],
    "vertex_label": [subgraph.vs[i]['label'] for i in range(len(subgraph.vs))],
    "vertex_label_size": 8,  # Smaller font to reduce overlap
    "vertex_label_dist": 1.5,  # Adjust label position outward
    "edge_width": [w / 5 for w in subgraph.es['weight']],  # Thinner edges for clarity
    "layout": layout,
    "bbox": (1200, 900),  # Larger figure size
    "margin": 100  # More margin to prevent overlap
}

# Plot and save
try:
    ig.plot(subgraph, **visual_style, target='author_communities_improved.png')
    print("Improved graph saved as 'author_communities_improved.png'")
except AttributeError as e:
    print(f"Plotting failed: {e}. Please ensure pycairo or cairocffi is installed.")