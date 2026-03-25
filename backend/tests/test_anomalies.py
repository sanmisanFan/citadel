import pytest
import json
from pathlib import Path

from CITation.anomalies.gpt_relevance import (
    process_citation_mentions,
    assign_scores_to_enriched_papers,
)
from CITation.anomalies.author_sus import build_suspicious_authors_graph
from CITation.anomalies.detect_anomalies import find_anomalies
from CITation.anomalies.venue_sus import detect_suspicious_venues

from CITation.data.process_references import process_markdown_string
from CITation.data.citation_graph_builder import extract_info

data_dir = Path(__file__).parent / "data"


@pytest.mark.slow
def test_citation_relevance(test_md, gpt_client):
    reference_mentions, raw_references = process_markdown_string(test_md)
    with open(data_dir / "enriched.json", "r") as f:
        enriched = json.load(f)

    trunced_ref_mentions = {}
    for x in reference_mentions.keys():
        if x in [1, 2, 3, 4, 5]:
            trunced_ref_mentions[x] = reference_mentions[x]

    citation_assessments = process_citation_mentions(
        trunced_ref_mentions, enriched, gpt_client
    )
    # why not just update this in process_citation_mentions?
    # or better yet, just keep these as separate objects?
    updated_enriched_papers = assign_scores_to_enriched_papers(
        enriched, citation_assessments
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


def test_sus_venues(test_paper_metadata):
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)
    export_data_suspicious, export_data_hop, scc_details = detect_suspicious_venues(
        citations, venues
    )

    print(export_data_suspicious, export_data_hop, scc_details)
