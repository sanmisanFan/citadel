import pytest
import json
from pathlib import Path

from CITation.anomalies.gpt_relevance import (
    process_citation_mentions,
    assign_scores_to_enriched_papers,
)
from CITation.anomalies.author_sus import build_suspicious_authors_graph
from CITation.anomalies.detect_anomalies import (
    build_anchors_from_mention,
    find_anomalies,
    generate_anomalous_json,
    generate_scc_anomalies,
)
from CITation.anomalies.venue_sus import detect_suspicious_venues

from CITation.data.process_references import process_markdown_string
from CITation.data.citation_graph_builder import extract_info

data_dir = Path(__file__).parent / "data"


@pytest.mark.slow
def test_citation_relevance(
    sample_enriched, sample_entity_keys, sample_refs_and_mentions, gpt_client
):
    ref_mentions, _ = sample_refs_and_mentions

    citation_assessments = process_citation_mentions(
        ref_mentions, sample_enriched, gpt_client
    )

    updated_enriched_papers = assign_scores_to_enriched_papers(
        sample_enriched, citation_assessments
    )

    with open(data_dir / "updated_enriched.json", "w") as f:
        json.dump(updated_enriched_papers, f)


def test_sus_authors(test_paper_metadata):
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)
    suspicious_sccs_g, sus_hop1_sccs, sccs_info = build_suspicious_authors_graph(
        authors, citations
    )

    print(suspicious_sccs_g, sus_hop1_sccs, sccs_info)


def test_anomalies(test_paper_metadata):
    with open(data_dir / "updated_enriched.json", "r") as f:
        enriched = json.load(f)
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)
    suspicious_sccs_g, sus_hop1_sccs, sccs_info = build_suspicious_authors_graph(
        authors, citations
    )
    anomalies = find_anomalies(enriched, sus_hop1_sccs, citations)
    print(anomalies)


def test_build_anchors_from_mention_emits_one_anchor_per_occurrence():
    text = "Prior work [3] improved results. Follow-up studies [3] replicated them."
    mention = {
        "text": text,
        "occurrences": [
            {
                "char_offset": text.index("[3]"),
                "page": 2,
                "marker_bbox": {"x": 10, "y": 20, "width": 5, "height": 6},
                "page_width": 612,
                "page_height": 792,
                "ref_label": "[3]",
            },
            {
                "char_offset": text.rindex("[3]"),
                "page": 4,
                "marker_bbox": {"x": 30, "y": 40, "width": 5, "height": 6},
                "page_width": 612,
                "page_height": 792,
                "ref_label": "[3]",
            },
        ],
    }

    anchors = build_anchors_from_mention(mention)

    assert len(anchors) == 2
    assert anchors[0]["page"] == 2
    assert anchors[0]["sentence"] == "Prior work [3] improved results."
    assert anchors[0]["ref_label"] == "[3]"
    assert anchors[1]["page"] == 4
    assert anchors[1]["sentence"] == "Follow-up studies [3] replicated them."
    assert anchors[1]["ref_label"] == "[3]"


def test_generate_anomalous_json_uses_first_anchor_page():
    text = "Prior work [8] improved results. Follow-up studies [8] replicated them."
    enriched = {
        "paper-1": {
            "citation_key": "citation-8",
            "reference_mentions": [
                {
                    "text": text,
                    "relevance_score": 2,
                    "assessment": "Explanation: score: 2 Weak support.",
                    "occurrences": [
                        {
                            "char_offset": text.index("[8]"),
                            "page": 6,
                            "marker_bbox": {"x": 11, "y": 22, "width": 5, "height": 6},
                            "page_width": 612,
                            "page_height": 792,
                            "ref_label": "[8]",
                        },
                        {
                            "char_offset": text.rindex("[8]"),
                            "page": 9,
                            "marker_bbox": {"x": 33, "y": 44, "width": 5, "height": 6},
                            "page_width": 612,
                            "page_height": 792,
                            "ref_label": "[8]",
                        },
                    ],
                }
            ],
        }
    }

    anomalous = generate_anomalous_json(enriched)
    issue = anomalous["identifiedIssue"][0]

    assert issue["page"] == 6
    assert issue["page"] == issue["anchors"][0]["page"]
    assert [anchor["page"] for anchor in issue["anchors"]] == [6, 9]
    assert issue["explanation"] == "Weak support."


def test_generate_scc_anomalies_collects_all_anchor_pages_and_keeps_primary_page():
    text_one = "The manuscript discusses prior work [5]."
    text_two = "Replication evidence for [5] appears later."
    citations = {
        "citation-0": {
            "author": ["author-1"],
            "hop": 0,
            "title": "Current Manuscript",
            "cite_number": 0,
            "venue": None,
        },
        "citation-5": {
            "author": ["author-1"],
            "hop": 1,
            "title": "Prior Work",
            "cite_number": 5,
            "venue": None,
        },
    }
    enriched = {
        "paper-5": {
            "citation_key": "citation-5",
            "reference_mentions": [
                {
                    "text": text_one,
                    "occurrences": [
                        {
                            "char_offset": text_one.index("[5]"),
                            "page": 3,
                            "marker_bbox": {"x": 10, "y": 10, "width": 5, "height": 6},
                            "page_width": 612,
                            "page_height": 792,
                            "ref_label": "[5]",
                        }
                    ],
                },
                {
                    "text": text_two,
                    "occurrences": [
                        {
                            "char_offset": text_two.index("[5]"),
                            "page": 7,
                            "marker_bbox": {"x": 20, "y": 20, "width": 5, "height": 6},
                            "page_width": 612,
                            "page_height": 792,
                            "ref_label": "[5]",
                        }
                    ],
                },
            ],
        }
    }
    hop1_sccs_data = {
        "nodes": [{"id": "author-1", "group": 1}],
        "links": [],
    }

    anomalies = generate_scc_anomalies(
        hop1_sccs_data,
        citations,
        enriched,
        existing_issue_ids=set(),
    )

    assert len(anomalies) == 1
    issue = anomalies[0]
    assert issue["category"]["name"] == "selfCitation"
    assert issue["page"] == 3
    assert issue["page"] == issue["anchors"][0]["page"]
    assert [anchor["page"] for anchor in issue["anchors"]] == [3, 7]


def test_sus_venues(test_paper_metadata):
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)
    export_data_suspicious, export_data_hop, scc_details = detect_suspicious_venues(
        citations, venues
    )

    print(export_data_suspicious, export_data_hop, scc_details)
