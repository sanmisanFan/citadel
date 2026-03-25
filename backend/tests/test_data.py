from CITation.data.process_references import (
    process_markdown_string,
    extract_references_section,
)
from CITation.data.raw_ref_to_json import PaperProcessor


from CITation.data.citation_graph_builder import extract_info, build_author_graph

from pathlib import Path
import pytest
import json

from CITation.anomalies.author_sus import build_suspicious_authors_graph

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


def test_extraction(test_paper_metadata):
    with open(data_dir / "entity_keys.json", "r") as f:
        entity_keys = json.load(f)

    citations, authors, venues = extract_info(entity_keys, test_paper_metadata)

    print(citations)
    print(authors)
    print(venues)

    ag = build_author_graph(citations)
    print(ag)
