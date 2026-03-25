from CITation.data.process_references import (
    process_markdown_string,
    extract_references_section,
)
from CITation.data.raw_ref_to_json import PaperProcessor
from CITation.data.gpt_relevance import (
    process_citation_mentions,
    assign_scores_to_enriched_papers,
)

from CITation.data.citation_graph_builder import extract_info, build_author_graph

from pathlib import Path
import pytest
import json

from CITation.data.author_sus import build_suspicious_authors_graph

data_dir = Path(__file__).parent / "data"


# test that we correctly detect when there are no references in a paper
def test_process_references_no_references(sample_no_ref):
    with pytest.raises(ValueError):
        process_markdown_string(sample_no_ref)


def test_process_references(test_md):
    reference_mentions, raw_references = process_markdown_string(test_md)
    print(reference_mentions, raw_references)


@pytest.mark.slow
def test_paper_processor(test_md, gpt_client):
    reference_mentions, raw_references = process_markdown_string(test_md)

    pp = PaperProcessor(gpt_client)
    enriched, entity_keys = pp.process_papers(raw_references[:5], reference_mentions)

    print(enriched)
    with open(data_dir / "enriched.json", "w") as f:
        json.dump(enriched, f)

    with open(data_dir / "entity_keys.json", "w") as f:
        json.dump(entity_keys, f)


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


def test_extraction(test_paper_metadata):
    with open(data_dir / "enriched.json", "r") as f:
        enriched = json.load(f)

    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)

    print(citations)
    print(authors)
    print(venues)

    ag = build_author_graph(citations)
    print(ag)


def test_sus_authors(test_paper_metadata):
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)
    suspicious_sccs_g, sus_hop1_sccs, sccs_info = build_suspicious_authors_graph(
        authors, citations
    )

    print(suspicious_sccs_g, sus_hop1_sccs, sccs_info)
