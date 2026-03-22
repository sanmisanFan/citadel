import tempfile
from pathlib import Path
import uuid
from pymupdf4llm import to_markdown
import fitz  # PyMuPDF


def pdf_to_str(content) -> str:
    """Converts a PDF to plain text via PyMuPDF.
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
