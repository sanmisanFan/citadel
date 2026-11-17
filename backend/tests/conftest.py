import pytest
from pathlib import Path
from CITation.data.utils import pdf_to_md_str
from CITation import llm
import json
from CITation.data.process_references import process_markdown_string

data_dir = Path(__file__).parent / "data"

# TODO: save the slow pipeline steps as fixtures and make them available here
# in test_conversion we should actually test the generation process


@pytest.fixture
def sample_no_ref():
    with open(f"{data_dir}/sample_no_ref.md", "r") as f:
        txt = f.read()
    return txt


@pytest.fixture
def sample():
    with open(f"{data_dir}/sample.md", "r") as f:
        txt = f.read()
    return txt


@pytest.fixture
def test_md():
    with open(f"{data_dir}/test.md", "r") as f:
        txt = f.read()
    return txt


@pytest.fixture
def sample_refs_and_mentions(sample):
    return process_markdown_string(sample)


@pytest.fixture
def sample_enriched():
    with open(data_dir / "sample_enriched.json", "r") as f:
        enriched = json.load(f)
    return enriched


@pytest.fixture
def sample_entity_keys():
    with open(data_dir / "sample_entity_keys.json", "r") as f:
        entity_keys = json.load(f)
    return entity_keys


@pytest.fixture
def test_paper_metadata():
    return {
        "title": "A Demo Manuscript as a ReviewerApp Study Case",
        "authors": ["Han Solo", "Luke Skywalker", "Obi-Wan Kenobi"],
        "year": "2026",
    }


@pytest.fixture(scope="session")
def gpt_client():
    if not llm.has_token():
        raise ValueError(
            f"Cannot run tests without a CreateAI token. Please set ${llm.TOKEN_ENV} first."
        )
    return llm.make_client()
