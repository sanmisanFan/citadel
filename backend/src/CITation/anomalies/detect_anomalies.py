import re


# Lowercase tokens that look like sentence terminators but aren't. The
# splitter consults this set when it sees a period; we don't try to be
# exhaustive, just to dodge the common scientific-writing offenders that
# tripped the previous naive splitter (e.g. citations next to "Fig.",
# "e.g.", or "et al.").
_SENTENCE_ABBREVIATIONS = frozenset(
    {
        "e.g",
        "i.e",
        "et al",
        "fig",
        "figs",
        "vs",
        "etc",
        "cf",
        "viz",
        "p",
        "pp",
        "vol",
        "no",
        "ed",
        "eds",
        "trans",
        "ref",
        "refs",
        "approx",
        "u.s",
        "u.k",
        "ph.d",
        "m.d",
        "mr",
        "mrs",
        "ms",
        "dr",
        "st",
        "ave",
        "no",
        "tab",
        "eq",
        "eqs",
        "sec",
        "ch",
    }
)


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Split text into sentences and return ``(start, end)`` spans into ``text``.

    Aware of the common scientific-writing abbreviations that the previous
    splitter mis-handled (``Fig.``, ``e.g.``, ``et al.``). Also avoids
    splitting after a single-letter capitalised token (initials) and inside
    bracketed citations like ``[1,2,3].`` followed by lowercase.
    """
    if not text:
        return []

    spans: list[tuple[int, int]] = []
    start = 0
    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        if ch in ".!?":
            # Look backwards for the immediate preceding token (letters/dot)
            # to test against the abbreviation set.
            j = i - 1
            while j >= 0 and (text[j].isalpha() or text[j] == "."):
                j -= 1
            token = text[j + 1 : i].lower()

            # Look ahead past closing brackets/quotes for the gap and the
            # following character — a sentence break needs whitespace then
            # a capital letter (or end of string).
            k = i + 1
            while k < n and text[k] in ")]}\"'":
                k += 1
            gap_end = k
            while gap_end < n and text[gap_end].isspace():
                gap_end += 1
            next_char = text[gap_end] if gap_end < n else ""

            is_terminator = True
            if token in _SENTENCE_ABBREVIATIONS:
                is_terminator = False
            elif ch == "." and len(token) == 1 and token.isalpha():
                # Single-letter abbreviation / initial (e.g. "J. Smith").
                is_terminator = False
            elif gap_end == n:
                # End of text — record whatever's left as the final sentence.
                is_terminator = True
            elif next_char and not (next_char.isupper() or next_char.isdigit() or next_char in "[("):
                is_terminator = False

            if is_terminator:
                spans.append((start, k))
                start = gap_end
                i = gap_end
                continue
        i += 1

    if start < n:
        spans.append((start, n))
    return spans


def sentence_at_offset(text: str, offset: int) -> str:
    """Return the sentence in ``text`` that contains ``offset``.

    Never returns ``""`` for a non-empty ``text``: if the offset falls
    outside every detected sentence span (shouldn't happen with the
    splitter above, but defensively guarded) we fall back to a 200-char
    window around the offset.
    """
    if not text:
        return ""
    offset = max(0, min(offset, len(text)))
    for s, e in split_sentences(text):
        if s <= offset < e:
            return text[s:e].strip()
    # Fallback window.
    lo = max(0, offset - 100)
    hi = min(len(text), offset + 100)
    return text[lo:hi].strip()


def build_anchors_from_mention(mention: dict) -> list[dict]:
    """Convert a grobid mention record into per-marker anchor dicts.

    Each anchor is what the frontend's ``resolveAnomalyAnchor`` consumes:
    a page, a normalized marker bbox (when grobid had coords), the sentence
    that contains the marker, and the marker's visible label.

    When a mention has no ``occurrences`` (older shape from the
    markdown-fallback parser, which doesn't track marker positions), we
    fall back to a single anchor with no bbox so the frontend can still
    try sentence-fuzzy + ``[N]`` scan.
    """
    text = mention.get("text", "") or ""
    occurrences = mention.get("occurrences") or []

    if not occurrences:
        return [
            {
                "page": mention.get("page"),
                "marker_bbox": None,
                "page_width": None,
                "page_height": None,
                "ref_label": None,
                "sentence": text.strip(),
            }
        ]

    anchors: list[dict] = []
    for occ in occurrences:
        sentence = sentence_at_offset(text, occ.get("char_offset", 0))
        anchors.append(
            {
                "page": occ.get("page"),
                "marker_bbox": occ.get("marker_bbox"),
                "page_width": occ.get("page_width"),
                "page_height": occ.get("page_height"),
                "ref_label": occ.get("ref_label"),
                "sentence": sentence,
            }
        )
    return anchors


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

                anchors = build_anchors_from_mention(mention)
                # Primary page for the card display is the first anchor's
                # page; the frontend uses individual anchors to scroll.
                page_num = anchors[0]["page"] if anchors else mention.get("page", 1)

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
                    "page": page_num,
                    "explanation": final_explanation,
                    "anchors": anchors,
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
            # Build anchors from every paragraph that mentions this citation,
            # so a self-citation that's referenced from three different
            # paragraphs lights up all three markers, not just the first.
            anchors: list[dict] = []
            paper = citation_key_to_paper.get(citation_key)
            if paper:
                for mention in paper.get("reference_mentions", []) or []:
                    anchors.extend(build_anchors_from_mention(mention))
            page_num = anchors[0]["page"] if anchors else 1

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
                "anchors": anchors,
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
            "anchors": [],
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
