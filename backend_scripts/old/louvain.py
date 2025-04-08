import json
import networkx as nx
import matplotlib.pyplot as plt

# For the Louvain algorithm (python-louvain package):
import community as community_louvain  # sometimes it's imported simply as 'community'

#############################################################################
# 1. Load your JSON data
#############################################################################
with open('./outputs/authors_updated.json', 'r') as f:
    authors_data = json.load(f)

with open('./outputs/citations_updated.json', 'r') as f:
    citations_data = json.load(f)

#############################################################################
# 2. Create a directed graph
#############################################################################
G_directed = nx.DiGraph()

#############################################################################
# 3. Build lookup dictionaries
#############################################################################
author_to_name = {
    author["id"]: author["standardized_name"]
    for author in authors_data["authors"]
}
citation_to_authors = {
    citation["id"]: citation["author"]
    for citation in citations_data["citations"]
}

#############################################################################
# 4. Add weighted edges based on citation relationships (same as before)
#############################################################################
for citation in citations_data["citations"]:
    citing_author_ids = citation["author"]
    cited_citation_ids = citation["citation_graph"]
    
    for cited_citation_id in cited_citation_ids:
        if cited_citation_id in citation_to_authors:
            cited_author_ids = citation_to_authors[cited_citation_id]
            for citing_author_id in citing_author_ids:
                for cited_author_id in cited_author_ids:
                    if G_directed.has_edge(citing_author_id, cited_author_id):
                        G_directed[citing_author_id][cited_author_id]['weight'] += 1
                    else:
                        G_directed.add_edge(citing_author_id, cited_author_id, weight=1)

#############################################################################
# 5. Convert Directed -> Undirected for Louvain
#############################################################################
# Louvain, in its common python-louvain form, expects an undirected graph.
# We'll sum weights in both directions if they exist, or just keep them as is.

G = nx.Graph()

for u, v, data in G_directed.edges(data=True):
    w = data.get('weight', 1)
    if G.has_edge(u, v):
        # If there's already an edge, add to the weight
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w)

#############################################################################
# 6. Run Louvain Community Detection
#############################################################################
# This returns a dict: node -> community_id
partition = community_louvain.best_partition(G, weight='weight')

# 'partition' might look like: {node1: 0, node2: 1, node3: 0, ...}
# meaning node1 is in community 0, node2 is in community 1, etc.

#############################################################################
# 7. Visualize the Graph with Communities
#############################################################################
plt.figure(figsize=(12, 8))

pos = nx.spring_layout(G, k=0.5, iterations=50)

# Edges
edge_weights = [d['weight'] for _,_,d in G.edges(data=True)]
edge_widths = [w * 0.5 for w in edge_weights]  # scale for visibility
nx.draw_networkx_edges(G, pos, alpha=0.3, width=edge_widths, arrows=False)

# Nodes, colored by community
# We'll gather unique community IDs first.
community_ids = set(partition.values())

# We can create a color map using matplotlib
import matplotlib.cm as cm
import numpy as np
cmap = list(cm.rainbow(np.linspace(0, 1, len(community_ids))))

for c_id, color in zip(community_ids, cmap):
    # Get all nodes in this community
    c_nodes = [n for n, cid in partition.items() if cid == c_id]
    # Draw them
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=c_nodes,
        node_color=[color],
        node_size=800,
        label=f'Community {c_id}'
    )

# Labels (using author names)
labels_for_plot = {node: author_to_name.get(node, str(node)) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels_for_plot, font_size=8, font_weight='bold')

plt.title("Louvain Communities (Undirected View of Citation Graph)")
plt.legend()
plt.show()

#############################################################################
# 8. Build a JSON export for the Louvain communities
#############################################################################
# Similar structure to your original script’s exports:
# We'll store each node with a 'group' = partition[node].
# We'll store edges with their final weight.

louvain_export_data = {
    "nodes": [
        {"id": node, "group": partition[node]}
        for node in G.nodes()
    ],
    "links": [
        {"source": u, "target": v, "value": data["weight"]}
        for u, v, data in G.edges(data=True)
    ]
}

output_json_path = "./outputs/louvain_communities.json"
with open(output_json_path, "w") as f:
    json.dump(louvain_export_data, f, indent=2)

print(f"\n✅ Louvain community data saved to: {output_json_path}")

#############################################################################
# 9. (Optional) Print modularity
#############################################################################
modularity_value = community_louvain.modularity(partition, G)
print(f"Modularity: {modularity_value:.4f}")
