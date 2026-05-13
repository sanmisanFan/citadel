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

    # The citation marker is nowhere in the paragraph GROBID handed us.
    # Returning the first 200 chars here mis-attributes every such anomaly
    # to the paragraph's opening, so distinct anomalies collide on a single
    # sentence the frontend then can't locate. Better to surface "no body
    # location" so the UI can fall back to the citation-marker bbox.
    return ""


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
                    "displayName": "Citation Anomaly",
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
      1) Self-citation (a cited author is also an author of the manuscript).
      2) Citation ring (cited author shares an SCC group with manuscript authors
         but isn't on the manuscript itself).
    Returns the updated data in memory (does NOT write a file).
    """

    # Build a lookup: author -> SCC group
    author_to_group = {}
    for node in hop1_sccs_data.get("nodes", []):
        author_to_group[node["id"]] = node.get("group", 0)

    citation_to_authors = {c_id: c["author"] for c_id, c in citations.items()}

    # Manuscript (hop-0) authors — only these qualify as "self" for self-citation.
    hop0_author_ids = set()
    for c in citations.values():
        if c.get("hop") == 0:
            hop0_author_ids.update(c.get("author", []))

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
                    if author_id in hop0_author_ids:
                        category_options["selfCitation"] = True
                        print(
                            f"{cited_paper_id}: Marked as selfCitation (author {author_id} is on the manuscript)."
                        )
                    else:
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
                # Self-citation only when the cited author is on the manuscript (hop-0).
                if author_id in hop0_author_ids:
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
                "displayName": "Citation Anomaly",
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


def generate_unreferenced_anomalies(enriched_papers, next_issue_id):
    """
    Flag references that appear in the bibliography but are never cited in the
    body of the manuscript (i.e. no reference_mentions). Returns a list of
    issues with category "unreferenced".
    """
    anomalous_issues = []
    issue_id = next_issue_id

    for paper in enriched_papers.values():
        citation_key = paper.get("citation_key")
        if not citation_key:
            continue
        mentions = paper.get("reference_mentions", []) or []
        if mentions:
            continue

        cite_number = paper.get("cite_number", "?")
        title = paper.get("title", "Unknown title")
        explanation = (
            f"[{cite_number}] Unreferenced bibliography entry.\n"
            f"This reference is listed in the bibliography but never cited in the body of the manuscript.\n"
            f"Title: \"{title[:80]}{'...' if len(title) > 80 else ''}\""
        )

        issue = {
            "id": f"issue-{issue_id}",
            "name": "citation",
            "displayName": "Citation Anomaly",
            "category": {
                "name": "unreferenced",
                "displayName": "Unreferenced",
                "options": {
                    "citationRing": False,
                    "selfCitation": False,
                    "unreferenced": True,
                },
            },
            "paper": [citation_key],
            "page": None,
            "explanation": explanation,
            "sentence": [{"sentence": "", "bbox": None}],
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

    for issue in scc_anomalies:
        for paper_key in issue.get("paper", []):
            existing_paper_ids.add(paper_key)

    # Skip papers that already have an anomaly so we don't double-flag.
    remaining_enriched = {
        ref_id: paper
        for ref_id, paper in enriched.items()
        if paper.get("citation_key") not in existing_paper_ids
    }
    next_issue_id = max(
        [int(issue["id"].split("-")[1]) for issue in anomalous_data["identifiedIssue"]]
        + [0]
    ) + 1
    unreferenced = generate_unreferenced_anomalies(remaining_enriched, next_issue_id)
    anomalous_data["identifiedIssue"].extend(unreferenced)

    return anomalous_data
