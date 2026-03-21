import pytest
from pathlib import Path
from CITation.data.utils import pdf_to_md_str

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
