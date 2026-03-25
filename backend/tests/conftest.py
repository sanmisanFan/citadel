import pytest
from pathlib import Path
from CITation.data.utils import pdf_to_md_str
from openai import OpenAI
import os

data_dir = Path(__file__).parent / "data"


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
def test_paper_metadata():
    return {
        "title": "A Demo Manuscript as a ReviewerApp Study Case",
        "authors": ["Han Solo", "Luke Skywalker", "Obi-Wan Kenobi"],
        "year": "2026",
    }


@pytest.fixture(scope="session")
def gpt_client():
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError(
            "Cannot run tests without valid OpenAI API key. Please set $OPENAI_API_KEY first."
        )
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
