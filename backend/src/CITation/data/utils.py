import tempfile
from pathlib import Path
import uuid
from pymupdf4llm import to_markdown
import fitz  # PyMuPDF


def pdf_to_md_str(content) -> str:
    doc = fitz.open(stream=content, filetype="pdf")

    res = to_markdown(doc, ignore_graphics=True, ignore_images=True, show_progress=True)
    return res
