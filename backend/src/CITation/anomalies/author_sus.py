import json
import networkx as nx
import matplotlib.pyplot as plt
from ..data.utils import get_citation_keys


# using the updated data from extraction
def build_suspicious_authors_graph(authors, citations):
    # 2. Create a directed graph
    G = nx.DiGraph()

    # 3. Build lookup dictionaries
    author_to_name = {author["id"]: author["standardized_name"] for author in authors}
    citation_to_authors = {
        c_key: citation["authors"] for c_key, citation in citations.items()
    }

    # 4. Add weighted edges based on citation relationships
    for citation in citations.values():
        citing_author_ids = citation["authors"]
        cited_citation_ids = get_citation_keys(citation)

        for cited_citation_id in cited_citation_ids:
            if cited_citation_id in citation_to_authors:
                cited_author_ids = citation_to_authors[cited_citation_id]
                for citing_author_id in citing_author_ids:
                    for cited_author_id in cited_author_ids:
                        if G.has_edge(citing_author_id, cited_author_id):
                            G[citing_author_id][cited_author_id]["weight"] += 1
                        else:
                            G.add_edge(citing_author_id, cited_author_id, weight=1)

    # 5. Find strongly connected components (SCCs)
    sccs = list(nx.strongly_connected_components(G))

    # 6. Define "suspicious" as SCCs of size 1-8 with any edge > weight_threshold
    weight_threshold = 1
    suspicious_sccs = []
    for scc in sccs:
        if 1 <= len(scc) <= 8:
            subgraph = G.subgraph(scc)
            if any(
                data["weight"] > weight_threshold
                for _, _, data in subgraph.edges(data=True)
            ):
                suspicious_sccs.append(scc)

    # 7. Identify hop-0 and hop-1 authors
    hop0_citation_ids = {c_id for c_id, c in citations.items() if c.get("hop") == 0}
    hop1_citation_ids = {c_id for c_id, c in citations.items() if c.get("hop") == 1}

    author_to_citations = {
        author["id"]: set(author.get("citation", [])) for author in authors
    }

    hop0_authors = {
        aid for aid, cits in author_to_citations.items() if cits & hop0_citation_ids
    }
    hop1_authors = {
        aid for aid, cits in author_to_citations.items() if cits & hop1_citation_ids
    }
    hop0_or_hop1_authors = hop0_authors.union(hop1_authors)

    # 8. Filter suspicious SCCs with at least one hop-0 OR hop-1 author
    hop01_sccs = [
        scc for scc in suspicious_sccs if any(a in hop0_or_hop1_authors for a in scc)
    ]

    # 9. Print SCCs
    print("Original Suspicious SCCs (Size 1-8 with High Weights):")
    for i, scc in enumerate(suspicious_sccs, 1):
        print(f"SCC {i}: {scc}")
        for u, v, data in G.subgraph(scc).edges(data=True):
            print(f"  {u} -> {v}: weight = {data['weight']}")

    print("\nSuspicious SCCs (At Least One Hop-0 or Hop-1 Author):")
    for i, scc in enumerate(hop01_sccs, 1):
        print(f"SCC {i}: {scc}")
        for u, v, data in G.subgraph(scc).edges(data=True):
            print(f"  {u} -> {v}: weight = {data['weight']}")

    # 10. Create subgraphs for visualization
    suspicious_nodes = set().union(*suspicious_sccs) if suspicious_sccs else set()
    hop01_nodes = set().union(*hop01_sccs) if hop01_sccs else set()

    suspicious_subgraph = G.subgraph(suspicious_nodes) if suspicious_nodes else G
    hop01_subgraph = G.subgraph(hop01_nodes) if hop01_nodes else G

    # 11. Visualize original suspicious SCCs
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(suspicious_subgraph, k=0.5, iterations=50)
    weights = [
        suspicious_subgraph[u][v]["weight"] for u, v in suspicious_subgraph.edges()
    ]
    nx.draw(
        suspicious_subgraph,
        pos,
        labels={n: author_to_name.get(n, n) for n in suspicious_subgraph.nodes()},
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=8,
        font_weight="bold",
        edge_color=["red" if w > weight_threshold else "gray" for w in weights],
        width=[w * 2 for w in weights],
        arrows=True,
        arrowstyle="-|>",
        arrowsize=15,
    )
    plt.title("Original Suspicious Citation Patterns (Size 1-8)")
    plt.show()

    # 12. Visualize hop-0 or hop-1 SCCs
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(hop01_subgraph, k=0.5, iterations=50)
    weights = [hop01_subgraph[u][v]["weight"] for u, v in hop01_subgraph.edges()]
    nx.draw(
        hop01_subgraph,
        pos,
        labels={n: author_to_name.get(n, n) for n in hop01_subgraph.nodes()},
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=8,
        font_weight="bold",
        edge_color=["red" if w > weight_threshold else "gray" for w in weights],
        width=[w * 2 for w in weights],
        arrows=True,
        arrowstyle="-|>",
        arrowsize=15,
    )
    plt.title("Suspicious Citation Patterns (Hop-0 OR Hop-1 Author Involved)")
    plt.show()
    """

    # 13. Assign consistent group IDs
    scc_group_map = {}
    current_group_id = 1
    for scc in suspicious_sccs + hop01_sccs:
        key = frozenset(scc)
        if key not in scc_group_map:
            scc_group_map[key] = current_group_id
            current_group_id += 1

    node_group_suspicious = {node: 0 for node in G.nodes()}
    node_group_hop01 = {node: 0 for node in G.nodes()}

    for scc in suspicious_sccs:
        gid = scc_group_map[frozenset(scc)]
        for node in scc:
            node_group_suspicious[node] = gid

    for scc in hop01_sccs:
        gid = scc_group_map[frozenset(scc)]
        for node in scc:
            node_group_hop01[node] = gid

    suspicious_sccs_g = {
        "nodes": [{"id": n, "group": node_group_suspicious[n]} for n in G.nodes()],
        "links": [
            {"source": u, "target": v, "value": d["weight"]}
            for u, v, d in G.edges(data=True)
        ],
    }

    sus_hop1_sccs = {
        "nodes": [{"id": n, "group": node_group_hop01[n]} for n in G.nodes()],
        "links": [
            {"source": u, "target": v, "value": d["weight"]}
            for u, v, d in G.edges(data=True)
        ],
    }

    sccs_info = {
        "original_sccs": [
            {
                "group_id": scc_group_map[frozenset(scc)],
                "authors": [author_to_name.get(a, a) for a in scc],
                "author_ids": list(scc),
                "all_hop01": all(a in hop0_or_hop1_authors for a in scc),
                "edges": [
                    {"source": u, "target": v, "weight": G[u][v]["weight"]}
                    for u, v in G.subgraph(scc).edges()
                ],
            }
            for scc in suspicious_sccs
        ],
        "hop0_or_hop1_sccs": [
            {
                "group_id": scc_group_map[frozenset(scc)],
                "authors": [author_to_name.get(a, a) for a in scc],
                "author_ids": list(scc),
                "edges": [
                    {"source": u, "target": v, "weight": G[u][v]["weight"]}
                    for u, v in G.subgraph(scc).edges()
                ],
            }
            for scc in hop01_sccs
        ],
    }

    return suspicious_sccs_g, sus_hop1_sccs, sccs_info
