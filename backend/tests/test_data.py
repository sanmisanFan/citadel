from CITation.data.process_references import (
    process_markdown_string,
    extract_references_section,
)
import pytest


# test that we correctly detect when there are no references in a paper
def test_process_references_no_references(sample_no_ref):
    with pytest.raises(ValueError):
        process_markdown_string(sample_no_ref)


def test_process_references(test_md):
    reference_mentions, raw_references = process_markdown_string(test_md)
    print(reference_mentions, raw_references)
