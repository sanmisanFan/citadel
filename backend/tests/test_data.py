from CITation.data.process_references import (
    process_markdown_string,
    extract_references_section,
)
from CITation.data.raw_ref_to_json import PaperProcessor
from CITation.data.utils import get_doi

from pathlib import Path
import pytest
import json

data_dir = Path(__file__).parent / "data"


# test that we correctly detect when there are no references in a paper
def test_process_references_no_references(sample_no_ref):
    with pytest.raises(ValueError):
        process_markdown_string(sample_no_ref)


def test_process_references(test_md):
    reference_mentions, raw_references = process_markdown_string(test_md)
    print(reference_mentions, raw_references)


def test_get_doi(test_md):
    reference_mentions, raw_references = process_markdown_string(test_md)
    print(reference_mentions, raw_references)
    for x in raw_references:
        get_doi(x)


@pytest.mark.slow
def test_paper_processor(test_md):
    reference_mentions, raw_references = process_markdown_string(test_md)

    pp = PaperProcessor()
    enriched, entity_keys = pp.process_papers(raw_references[:5], reference_mentions)
    print("Number of papers processed: ", len(enriched), " ", len(entity_keys))

    print(enriched)
    with open(data_dir / "enriched.json", "w") as f:
        json.dump(enriched, f)

    with open(data_dir / "entity_keys.json", "w") as f:
        json.dump(entity_keys, f)
