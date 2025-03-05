import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data
with open('./outputs/authors.json', 'r') as f:
    authors_data = json.load(f)

with open('./outputs/citations.json', 'r') as f:
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
                    if G.has_edge(citing_name, cited_name):
                        G[citing_name][cited_name]['weight'] += 1
                    else:
                        G.add_edge(citing_name, cited_name, weight=1)

# Find strongly connected components
sccs = list(nx.strongly_connected_components(G))

# Define "suspicious" as SCCs with 2-5 authors and high weights
suspicious_sccs = []
weight_threshold = 1  # Adjust this threshold (e.g., >1 for multiple citations)
for scc in sccs:
    if 2 <= len(scc) <= 5:  # Small SCCs
        subgraph = G.subgraph(scc)
        # Check if any edge in the SCC has weight > threshold
        suspicious = False
        for u, v, data in subgraph.edges(data=True):
            if data['weight'] > weight_threshold:
                suspicious = True
                break
        if suspicious:
            suspicious_sccs.append(scc)

# Print suspicious SCCs
print("Suspicious Strongly Connected Components (Size 2-5 with High Weights):")
if suspicious_sccs:
    for i, scc in enumerate(suspicious_sccs, 1):
        print(f"Suspicious SCC {i}: {scc}")
        subgraph = G.subgraph(scc)
        for u, v, data in subgraph.edges(data=True):
            print(f"  {u} -> {v}: weight = {data['weight']}")
else:
    print("No suspicious SCCs found.")

# Create a subgraph of suspicious SCCs for visualization
suspicious_nodes = set().union(*suspicious_sccs)  # Combine all nodes from suspicious SCCs
suspicious_subgraph = G.subgraph(suspicious_nodes) if suspicious_nodes else G

# Prepare edge weights for visualization
edge_weights = [suspicious_subgraph[u][v]['weight'] for u, v in suspicious_subgraph.edges()]
edge_widths = [w * 2 for w in edge_weights]  # Scale for visibility
edge_colors = ['red' if w > weight_threshold else 'gray' for w in edge_weights]  # Highlight high weights

# Visualize the suspicious subgraph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(suspicious_subgraph, k=0.5, iterations=50)
nx.draw(suspicious_subgraph, pos, with_labels=True, node_color="lightblue", node_size=800, 
        font_size=8, font_weight="bold", edge_color=edge_colors, width=edge_widths, 
        arrows=True, arrowstyle="-|>", arrowsize=15)
plt.title("Suspicious Citation Patterns (Weighted Edges)")
plt.show()

# Optional: Print all edge weights in the full graph for inspection
print("\nAll Edge Weights in Full Graph (for reference):")
for u, v, data in sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True):
    print(f"{u} -> {v}: weight = {data['weight']}")