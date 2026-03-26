import json
import re


def generate_anomalous_json(enriched_papers):
    """
    Reads an enriched papers JSON file, extracts citations with low relevancy scores (1, 2, or 3 but not 0),
    cleans the explanation text by removing 'score: X' and 'Explanation:', and returns the anomalous data.

    Parameters:
        input_file (str): Path to the enriched papers JSON file.

    Returns:
        dict: A dictionary with all identified anomalous citation issues.
    """

    anomalous_issues = []
    issue_id = 1

    for paper in enriched_papers.values():
        citation_key = paper.get("citation_key", "unknown")

        for mention in paper.get("reference_mentions", []):
            relevance_score = mention.get("relevance_score", None)

            # Identify low relevancy citations (score 1, 2, or 3, but not 0)
            if relevance_score is not None and 0 < relevance_score <= 3:
                raw_explanation = mention.get("assessment", "No explanation provided.")

                # (1) Remove "score: X" text (case-insensitive)
                no_score = re.sub(r"(?i)\bscore:\s*\d+", "", raw_explanation).strip()

                # (2) Remove leading "Explanation:" (case-insensitive)
                cleaned_explanation = re.sub(
                    r"(?i)^Explanation:\s*", "", no_score
                ).strip()

                # Fallback if explanation is empty after cleaning
                final_explanation = (
                    cleaned_explanation
                    if cleaned_explanation
                    else "No explanation provided."
                )

                issue = {
                    "id": f"issue-{issue_id}",
                    "name": "citation",
                    "displayName": "Citation Anomalous",
                    "category": {
                        "name": "lowRelevancy",
                        "displayName": "Low Relevancy",
                        "options": {"citationRing": False, "selfCitation": False},
                    },
                    "paper": [citation_key],
                    "page": 1,  # Can be customized if you extract page info
                    "explanation": final_explanation,
                    "sentence": [{"sentence": mention.get("text", ""), "bbox": None}],
                }
                anomalous_issues.append(issue)
                issue_id += 1

    anomalous_json = {"identifiedIssue": anomalous_issues}
    return anomalous_json


def update_anomalous_with_hop1_sccs(anomalous_data, hop1_sccs_data, citations):
    """
    Updates the anomalous data by checking citations against hop-1 SCCs for:
      1) Self-citation (if an author cites themselves).
      2) Citation ring (if authors in group != 0 are citing each other).
    Returns the updated data in memory (does NOT write a file).
    """

    # Build a lookup: author -> SCC group
    author_to_group = {}
    for node in hop1_sccs_data.get("nodes", []):
        author_to_group[node["id"]] = node.get("group", 0)

    # (Optional) Build a set of edges (source, target) if your JSON includes "links"
    links_data = hop1_sccs_data.get("links", [])
    scc_edges = set()
    for edge in links_data:
        scc_edges.add((edge["source"], edge["target"]))

    citation_to_authors = {c_id: c["authors"] for c_id, c in citations.items()}

    # 3) Update each anomalous issue
    for issue in anomalous_data["identifiedIssue"]:
        category_options = issue["category"]["options"]

        # Each "issue" might reference multiple "paper" IDs
        for cited_paper_id in issue["paper"]:
            if cited_paper_id not in citation_to_authors:
                print(
                    f"Warning: Citation {cited_paper_id} not found in citations_updated.json. Skipping."
                )
                continue

            cited_authors = citation_to_authors[cited_paper_id]

            # Check if any cited author is in a group != 0
            for author_id in cited_authors:
                author_group = author_to_group.get(author_id, 0)

                if author_group != 0:
                    # SELF-CITATION: If there's an edge (author_id, author_id) in the SCC
                    if (author_id, author_id) in scc_edges:
                        category_options["selfCitation"] = True
                        print(
                            f"{cited_paper_id}: Marked as selfCitation (SCC edge from {author_id} to itself)."
                        )
                    else:
                        # CITATION RING
                        category_options["citationRing"] = True
                        print(
                            f"{cited_paper_id}: Marked as citationRing (author in SCC group {author_group})."
                        )

                    # Once flagged, no need to check more authors for this paper in this issue
                    break

    return anomalous_data


def find_anomalies(enriched, hop1_sccs_data, citations):
    anomalous_data = generate_anomalous_json(enriched)
    return update_anomalous_with_hop1_sccs(anomalous_data, hop1_sccs_data, citations)
