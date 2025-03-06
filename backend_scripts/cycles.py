import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data
with open('authors.json', 'r') as f:
    authors_data = json.load(f)

with open('citations.json', 'r') as f:
    citations_data = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Build lookup dictionaries
author_to_name = {author["id"]: author["standardized_name"] for author in authors_data["authors"]}
citation_to_authors = {citation["id"]: citation["author"] for citation in citations_data["citations"]}

# Add weighted edges based on citation relationships
for citation in citations_data["citations"]:
    citing_authors = citation["author"]
    cited_ids = citation["citation_graph"]
    
    for cited_id in cited_ids:
        if cited_id in citation_to_authors:  # Only process known citations
            cited_authors = citation_to_authors[cited_id]
            for citing_author_id in citing_authors:
                for cited_author_id in cited_authors:
                    citing_name = author_to_name.get(citing_author_id, citing_author_id)
                    cited_name = author_to_name.get(cited_author_id, cited_author_id)
                    # If edge exists, increment weight; otherwise, add with weight 1
                    if G.has_edge(citing_name, cited_name):
                        G[citing_name][cited_name]['weight'] += 1
                    else:
                        G.add_edge(citing_name, cited_name, weight=1)

# Find strongly connected components
sccs = list(nx.strongly_connected_components(G))

# Print SCCs
print("Strongly Connected Components:")
for i, scc in enumerate(sccs, 1):
    print(f"SCC {i}: {scc}")

# Prepare edge weights for visualization
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
# Normalize weights for edge thickness (e.g., scale between 1 and 10)
edge_widths = [w * 2 for w in edge_weights]  # Multiply by 2 for visibility

# Visualize the graph
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=0.3, iterations=50)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=8, 
        font_weight="bold", edge_color="gray", width=edge_widths, arrows=True, 
        arrowstyle="-|>", arrowsize=15)
plt.title("Weighted Author Citation Graph (Who Cited Whom)")
plt.show()

# Optional: Print edge weights for inspection
print("\nEdge Weights:")
for u, v, data in G.edges(data=True):
    print(f"{u} -> {v}: weight = {data['weight']}")