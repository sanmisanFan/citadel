import json
import re


def extract_citation_sentence(text, citation_key):
    """
    Extract just the sentence containing the citation marker from a text excerpt.

    Args:
        text: Full text excerpt
        citation_key: Citation key like "citation-5" or just "5"

    Returns:
        The sentence containing the citation, or a truncated version if not found
    """
    if not text:
        return ""

    # Extract the number from citation key
    cite_num = citation_key.replace("citation-", "") if "citation-" in citation_key else citation_key

    # Pattern to find citation markers like [5], [5,6], etc.
    citation_pattern = rf'\[{cite_num}(?:,\s*\d+)*\]|\[(?:\d+,\s*)*{cite_num}(?:,\s*\d+)*\]'

    # Split text into sentences (simple split on . ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if re.search(citation_pattern, sentence):
            # Found a sentence with our citation
            return sentence.strip()

    # If citation not found in any sentence, return a truncated excerpt
    # Find the citation marker and extract surrounding context
    match = re.search(citation_pattern, text)
    if match:
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 100)
        return text[start:end].strip()

    # Last resort: return first 200 chars
    return text[:200].strip() + "..." if len(text) > 200 else text.strip()


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
                page_num = mention.get("page", 1)  # Get page number from mention

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

                # Extract just the sentence containing the citation, not the whole paragraph
                full_text = mention.get("text", "")
                sentence_text = extract_citation_sentence(full_text, citation_key)

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
                    "page": page_num,  # Use actual page number from citation mention
                    "explanation": final_explanation,
                    "sentence": [{"sentence": sentence_text, "bbox": None}],
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

    citation_to_authors = {c_id: c["author"] for c_id, c in citations.items()}

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


def generate_scc_anomalies(hop1_sccs_data, citations, enriched_papers, existing_issue_ids):
    """
    Create anomalies for citation rings/self-citations based on SCC data,
    even if the citations don't have low relevancy scores.
    """
    anomalous_issues = []
    issue_id = max([int(id.split("-")[1]) for id in existing_issue_ids] + [0]) + 1

    # Build a lookup: author -> SCC group
    author_to_group = {}
    for node in hop1_sccs_data.get("nodes", []):
        author_to_group[node["id"]] = node.get("group", 0)

    # Build a set of edges (source, target) with weights
    links_data = hop1_sccs_data.get("links", [])
    scc_edges = {}
    for edge in links_data:
        scc_edges[(edge["source"], edge["target"])] = edge.get("value", 1)

    citation_to_authors = {c_id: c["author"] for c_id, c in citations.items()}

    # Track which citations already have anomalies
    already_flagged = existing_issue_ids

    # Build a lookup from citation_key to enriched paper data
    citation_key_to_paper = {}
    for paper in enriched_papers.values():
        ck = paper.get("citation_key")
        if ck:
            citation_key_to_paper[ck] = paper

    # Get hop-0 (current paper being reviewed) authors
    hop0_author_ids = set()
    for c_id, c in citations.items():
        if c.get("hop") == 0:
            hop0_author_ids.update(c.get("author", []))

    # Check each hop-1 citation for SCC involvement
    for citation_key, citation in citations.items():
        hop = citation.get("hop")
        if hop != 1:
            continue

        # Skip if already has an anomaly
        if citation_key in already_flagged:
            continue

        cited_authors = citation.get("author", [])
        is_self_citation = False
        is_citation_ring = False
        overlapping_author_ids = []

        for author_id in cited_authors:
            author_group = author_to_group.get(author_id, 0)
            if author_group != 0:
                # Check if this author is also an author of the current paper (hop-0)
                if author_id in hop0_author_ids:
                    is_self_citation = True
                    overlapping_author_ids.append(author_id)
                elif (author_id, author_id) in scc_edges:
                    is_self_citation = True
                    overlapping_author_ids.append(author_id)
                else:
                    is_citation_ring = True

        if is_self_citation or is_citation_ring:
            # Find the mention text and page from enriched papers
            mention_text = ""
            page_num = 1
            paper = citation_key_to_paper.get(citation_key)
            if paper:
                mentions = paper.get("reference_mentions", [])
                if mentions:
                    full_text = mentions[0].get("text", "")
                    page_num = mentions[0].get("page", 1)
                    # Extract just the sentence containing the citation
                    mention_text = extract_citation_sentence(full_text, citation_key)

            category_name = "selfCitation" if is_self_citation else "citationRing"
            display_name = "Self Citation" if is_self_citation else "Citation Ring"

            # Get citation details for better explanation
            cite_number = citation.get("cite_number", "?")
            title = citation.get("title", "Unknown title")

            # Build informative explanation
            if is_self_citation:
                num_overlapping = len(overlapping_author_ids)
                explanation = (
                    f"[{cite_number}] Self-citation detected (hop-{hop} reference).\n"
                    f"{num_overlapping} author(s) of this reference are also authors of the manuscript being reviewed.\n"
                    f"Title: \"{title[:80]}{'...' if len(title) > 80 else ''}\""
                )
            else:
                explanation = (
                    f"[{cite_number}] Citation ring pattern detected (hop-{hop} reference).\n"
                    f"Authors of this paper show unusually high mutual citation rates with manuscript authors.\n"
                    f"Title: \"{title[:80]}{'...' if len(title) > 80 else ''}\""
                )

            issue = {
                "id": f"issue-{issue_id}",
                "name": "citation",
                "displayName": "Citation Anomalous",
                "category": {
                    "name": category_name,
                    "displayName": display_name,
                    "options": {
                        "citationRing": is_citation_ring,
                        "selfCitation": is_self_citation,
                    },
                },
                "paper": [citation_key],
                "page": page_num,
                "explanation": explanation,
                "sentence": [{"sentence": mention_text, "bbox": None}],
            }
            anomalous_issues.append(issue)
            issue_id += 1

    return anomalous_issues


def find_anomalies(enriched, hop1_sccs_data, citations):
    anomalous_data = generate_anomalous_json(enriched)
    anomalous_data = update_anomalous_with_hop1_sccs(anomalous_data, hop1_sccs_data, citations)

    # Get existing issue paper IDs to avoid duplicates
    existing_paper_ids = set()
    for issue in anomalous_data.get("identifiedIssue", []):
        for paper_key in issue.get("paper", []):
            existing_paper_ids.add(paper_key)

    # Generate additional anomalies for SCCs not already flagged
    scc_anomalies = generate_scc_anomalies(
        hop1_sccs_data, citations, enriched, existing_paper_ids
    )
    anomalous_data["identifiedIssue"].extend(scc_anomalies)

    return anomalous_data
