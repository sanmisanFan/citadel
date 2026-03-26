from pathlib import Path
from pymupdf4llm import to_markdown
import fitz  # PyMuPDF
# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict


def pdf_to_str(content) -> str:
    """Converts PDF bytes to plain text via PyMuPDF.
    Args:
        content (bytes): The contents of the PDF as bytes.

    Returns:
        A string containing the text content of the pdf.
    """
    doc = fitz.open(stream=content, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    return text


# this is pretty slow compared to just getting the text content because it uses OCR. I know the structure is useful, but at least
# for the references it might be better to use plain text. when I tried it, it puts REFERENCES on its own line and everything after
# is just references.
def pdf_to_md_str(content) -> str:
    """Converts a PDF to markdown via PyMuPDF. Used in the initial pre-processing step to
    get a structured text view of the data.

    Args:
        content (bytes): The contents of the PDF as bytes.

    Returns:
        A string containing the markdown version of the pdf.
    """
    doc = fitz.open(stream=content, filetype="pdf")

    res = to_markdown(doc, ignore_graphics=True, ignore_images=True, show_progress=True)
    return res


# doesn't work properly... wants openai version 1.109...
"""
def pdf_to_md_str_marker(content) -> str:
    fname = uuid.uuid4()

    # https://github.com/datalab-to/marker
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        pdf_path = tmpdir_path / f"{fname}.pdf"

        pdf_path.write_bytes(content)

        config = {
            "output_format": "markdown",
            "force_ocr": False,
            "strip_existing_ocr": False,
        }

        converter = PdfConverter(
            config=config,
            artifact_dict=create_model_dict(),
        )

        res = converter(pdf_path)
        return res
"""


def get_openalex_authors(openalex):
    return [
        {
            "name": authorship.get("author", {}).get("display_name"),
            "orcid": authorship.get("author", {}).get("orcid"),
        }
        for authorship in openalex.get("authorships", [])
    ]


def get_openalex_refs(openalex) -> list[str] | None:
    refs = openalex.get("referenced_works", []) + openalex.get("related_works", [])
    return refs if len(refs) > 0 else None


def get_citation_keys(citation):
    return [x.get("citation_key", "") for x in citation.get("enriched_references", [])]
