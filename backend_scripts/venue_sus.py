import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# 1. Load JSON data
citations_file = "./outputs/citations_updated.json"
venues_file = "./outputs/venues_updated.json"

with open(citations_file, "r", encoding="utf-8") as f:
    citations_data = json.load(f)

with open(venues_file, "r", encoding="utf-8") as f:
    venues_data = json.load(f)

# 2. Build basic lookups
citation_to_venue = {
    citation["id"]: citation["venue"]
    for citation in citations_data["citations"]
}
venue_to_name = {
    venue["id"]: venue["standardized_name"]
    for venue in venues_data["venues"]
}

# 3. Identify hop=0 and hop=1 venues
hop0_venues = set()
hop1_venues = set()

for citation in citations_data["citations"]:
    venue_id = citation.get("venue")
    hop_value = citation.get("hop", None)
    if venue_id is not None and hop_value is not None:
        if hop_value == 0:
            hop0_venues.add(venue_id)
        elif hop_value == 1:
            hop1_venues.add(venue_id)

# 4. Initialize a directed graph (venue-based)
G_venue = nx.DiGraph()

# 5. Count edges (venue→venue) with weights
venue_citation_counter = defaultdict(int)

for citation in citations_data["citations"]:
    citing_venue = citation["venue"]  # Venue of the citing paper
    cited_citation_ids = citation["citation_graph"]  # List of cited papers

    for cited_citation_id in cited_citation_ids:
        cited_venue = citation_to_venue.get(cited_citation_id)
        if citing_venue and cited_venue:
            venue_citation_counter[(citing_venue, cited_venue)] += 1

# 6. Add edges to the graph with weights
for (venue_src, venue_tgt), count in venue_citation_counter.items():
    G_venue.add_edge(venue_src, venue_tgt, weight=count)

# 7. Find strongly connected components (SCCs)
sccs = list(nx.strongly_connected_components(G_venue))

# 8. Define suspicious SCCs (size 1–5, any edge > threshold)
weight_threshold = 1
suspicious_sccs = []

for scc in sccs:
    if 1 <= len(scc) <= 5:
        subgraph = G_venue.subgraph(scc)
        # If any edge in subgraph has weight > threshold → suspicious
        if any(data["weight"] > weight_threshold for _, _, data in subgraph.edges(data=True)):
            suspicious_sccs.append(scc)

# 9. Among suspicious SCCs, pick those with at least one hop=0 OR at least one hop=1
hop_sccs = []
for scc in suspicious_sccs:
    # Now we use OR instead of AND
    if any(ven in hop0_venues for ven in scc) or any(ven in hop1_venues for ven in scc):
        hop_sccs.append(scc)

# 10. Print the results
print("Suspicious SCCs (size 1-5, edge weight > 1):")
if not suspicious_sccs:
    print("  None found.")
else:
    for i, scc in enumerate(suspicious_sccs, start=1):
        print(f"  SCC {i}: {scc}")

print("\nSuspicious SCCs with hop=0 OR hop=1 venues (ANY hop):")
if not hop_sccs:
    print("  None found.")
else:
    for i, scc in enumerate(hop_sccs, start=1):
        print(f"  SCC {i}: {scc}")

# 11. Create subgraph for visualization: "Any Hop" SCCs
hop_nodes = set().union(*hop_sccs) if hop_sccs else set()
hop_subgraph = G_venue.subgraph(hop_nodes)

if hop_nodes:
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(hop_subgraph, k=0.5, iterations=50)

    # Prepare edges
    edge_weights = [hop_subgraph[u][v]["weight"] for u, v in hop_subgraph.edges()]
    edge_widths = [w * 2 for w in edge_weights]
    edge_colors = ["red" if w > weight_threshold else "gray" for w in edge_weights]

    labels_for_plot = {node: venue_to_name.get(node, str(node)) for node in hop_subgraph.nodes()}

    nx.draw(
        hop_subgraph,
        pos,
        labels=labels_for_plot,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=8,
        font_weight="bold",
        edge_color=edge_colors,
        width=edge_widths,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=15
    )
    plt.title("Suspicious Venue SCCs with Hop=0 OR Hop=1 Venues (Any Hop)")
    plt.show()
else:
    print("\nNo hop-based SCCs to visualize (OR condition).")

# 12. Assign group IDs
node_group_suspicious = {node: 0 for node in G_venue.nodes()}
node_group_hop = {node: 0 for node in G_venue.nodes()}

for i, scc in enumerate(suspicious_sccs, start=1):
    for node in scc:
        node_group_suspicious[node] = i

for i, scc in enumerate(hop_sccs, start=1):
    for node in scc:
        node_group_hop[node] = i

# 13. Export suspicious SCCs (all suspicious) to JSON
export_data_suspicious = {
    "nodes": [
        {"id": node, "group": node_group_suspicious[node]}
        for node in G_venue.nodes()
    ],
    "links": [
        {"source": u, "target": v, "value": data["weight"]}
        for u, v, data in G_venue.edges(data=True)
    ]
}

output_json_suspicious = "./outputs/suspicious_venues.json"
with open(output_json_suspicious, "w", encoding="utf-8") as f:
    json.dump(export_data_suspicious, f, indent=2)

print(f"\n✅ All suspicious venue SCCs saved to: {output_json_suspicious}")

# 14. Export "Any Hop" SCCs to JSON
export_data_hop = {
    "nodes": [
        {"id": node, "group": node_group_hop[node]}
        for node in G_venue.nodes()
    ],
    "links": [
        {"source": u, "target": v, "value": data["weight"]}
        for u, v, data in G_venue.edges(data=True)
    ]
}

output_json_hop = "./outputs/hop_venues_any.json"
with open(output_json_hop, "w", encoding="utf-8") as f:
    json.dump(export_data_hop, f, indent=2)

print(f"✅ Hop=0 OR Hop=1 SCCs saved to: {output_json_hop}")

# 15. (Optional) Detailed SCC info
scc_details = {
    "all_suspicious_sccs": [
        {
            "group_id": i,
            "venue_ids": list(scc),
            "venue_names": [venue_to_name.get(v, str(v)) for v in scc],
            "contains_hop0": any(v in hop0_venues for v in scc),
            "contains_hop1": any(v in hop1_venues for v in scc),
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "weight": G_venue[u][v]["weight"]
                }
                for u, v in G_venue.subgraph(scc).edges()
            ]
        }
        for i, scc in enumerate(suspicious_sccs, start=1)
    ],
    "hop_sccs_any": [
        {
            "group_id": i,
            "venue_ids": list(scc),
            "venue_names": [venue_to_name.get(v, str(v)) for v in scc],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "weight": G_venue[u][v]["weight"]
                }
                for u, v in G_venue.subgraph(scc).edges()
            ]
        }
        for i, scc in enumerate(hop_sccs, start=1)
    ]
}

details_json_path = "./outputs/scc_details_with_hop_any.json"
with open(details_json_path, "w", encoding="utf-8") as f:
    json.dump(scc_details, f, indent=2)

print(f"✅ Detailed SCC info saved to: {details_json_path}")
