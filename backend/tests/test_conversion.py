from pathlib import Path
import pytest
from CITation.data.utils import pdf_to_md_str


@pytest.mark.slow
def test_convert_sample():
    data_dir = Path(__file__).parent / "data"
    with open(f"{data_dir}/sample.pdf", "rb") as f:
        pdf_bytes = f.read()

    fp = data_dir / "sample.md"
    res = pdf_to_md_str(pdf_bytes)
    with open(fp, "w") as f:
        f.write(res)


@pytest.mark.slow
def test_convert_sample_no_ref():
    data_dir = Path(__file__).parent / "data"
    with open(f"{data_dir}/Fake1.pdf", "rb") as f:
        pdf_bytes = f.read()

    fp = data_dir / "sample_no_ref.md"
    res = pdf_to_md_str(pdf_bytes)
    with open(fp, "w") as f:
        f.write(res)
