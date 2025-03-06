import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data
with open('./outputs/authors_updated.json', 'r') as f:
    authors_data = json.load(f)

with open('./outputs/citations_updated.json', 'r') as f:
    citations_data = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Build lookup dictionaries
author_to_name = {}
for author in authors_data["authors"]:
    # Use standardized_name if available, else raw_name
    display_name = author["standardized_name"] or author["raw_name"]
    author_to_name[author["id"]] = display_name

citation_to_authors = {}
for citation in citations_data["citations"]:
    citation_to_authors[citation["id"]] = citation["author"]

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

# -----------------------------------------------------------------------------
# 1) Extract all simple cycles (rings)
# -----------------------------------------------------------------------------
all_cycles = list(nx.simple_cycles(G))
print("\nALL SIMPLE CYCLES (RINGS) FOUND IN THE GRAPH:")
if all_cycles:
    for i, cycle in enumerate(all_cycles, 1):
        print(f"Cycle {i}: {cycle}")
else:
    print("No simple cycles found.")

# # -----------------------------------------------------------------------------
# # 2) For each author, create a subgraph with all nodes 'linked' to that author
# #    i.e. the union of the author's ancestors and descendants, plus itself.
# # -----------------------------------------------------------------------------
# # Build a reverse graph to find ancestors easily
# G_reverse = G.reverse(copy=False)

# author_linked_subgraphs = {}

# # We'll iterate over the unique author *names* that appear in the graph.
# unique_authors_in_graph = set(G.nodes())

# for author_name in unique_authors_in_graph:
#     # "Descendants" = all nodes reachable *from* this author
#     descendants = nx.descendants(G, author_name)
#     # "Ancestors"   = all nodes that can reach this author
#     ancestors = nx.descendants(G_reverse, author_name)
    
#     # The union of the author, its ancestors, and its descendants
#     linked_nodes = set([author_name]) | descendants | ancestors
    
#     # Create the induced subgraph
#     subG = G.subgraph(linked_nodes).copy()
    
#     # Store the subgraph in a dictionary for later use
#     # Here we store the adjacency as a simple dict of {node: [neighbors], ...}
#     adjacency_dict = {}
#     for node in subG.nodes():
#         adjacency_dict[node] = list(subG[node])
    
#     author_linked_subgraphs[author_name] = adjacency_dict

# # Example: Print out subgraph adjacency for one or two authors
# print("\nEXAMPLE SUBGRAPH FOR AN AUTHOR (FIRST IN GRAPH):")
# if unique_authors_in_graph:
#     example_author = next(iter(unique_authors_in_graph))
#     print(f"Author: {example_author}")
#     print("Linked subgraph adjacency:")
#     print(json.dumps(author_linked_subgraphs[example_author], indent=2))
# else:
#     print("No authors found in the graph.")

# # -----------------------------------------------------------------------------
# # OPTIONAL: You could write 'author_linked_subgraphs' to a JSON file
# # -----------------------------------------------------------------------------
# """
# with open("./outputs/author_subgraphs.json", "w", encoding="utf-8") as f:
#     json.dump(author_linked_subgraphs, f, indent=2)
# print("Wrote per-author subgraphs to author_subgraphs.json")
# """

# # -----------------------------------------------------------------------------
# # Visualization: You already have code to visualize suspicious subgraphs, etc.
# # If you'd like to visualize an individual author's subgraph, do something like:
# # -----------------------------------------------------------------------------
# """
# chosen_author = "Han Solo"  # or any name in G
# if chosen_author in author_linked_subgraphs:
#     chosen_adj = author_linked_subgraphs[chosen_author]
#     # Rebuild an nx.Graph from that adjacency
#     chosen_subG = nx.DiGraph()
#     for node, neighbors in chosen_adj.items():
#         for nbr in neighbors:
#             weight = G[node][nbr]['weight']  # use original G to get weight
#             chosen_subG.add_edge(node, nbr, weight=weight)

#     # Now visualize chosen_subG similarly to your suspicious subgraph code
#     plt.figure(figsize=(10, 8))
#     pos = nx.spring_layout(chosen_subG, k=0.5, iterations=50)
#     edge_weights = [chosen_subG[u][v]['weight'] for u, v in chosen_subG.edges()]
#     edge_colors = ['red' if w>1 else 'gray' for w in edge_weights]
#     edge_widths = [w*2 for w in edge_weights]

#     nx.draw(chosen_subG, pos, with_labels=True, node_color="lightblue",
#             node_size=800, font_size=8, font_weight="bold",
#             edge_color=edge_colors, width=edge_widths,
#             arrows=True, arrowstyle="-|>", arrowsize=15)

#     plt.title(f"Subgraph Linked to {chosen_author}")
#     plt.show()
# """

# print("\nDone! We’ve extracted all simple cycles and created subgraphs per author.")
