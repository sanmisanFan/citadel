import tempfile
from pathlib import Path
import uuid
from pymupdf4llm import to_markdown
import fitz  # PyMuPDF


def pdf_to_md_str(content):
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
