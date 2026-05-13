from pathlib import Path
from pymupdf4llm import to_markdown
import fitz  # PyMuPDF


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


def pdf_first_pages_text(content, n_pages: int = 2) -> str:
    """Return plain text from the first ``n_pages`` of a PDF.

    Used for fast manuscript metadata extraction (title/authors/year live on
    the first page; reading the whole document is wasteful for that lookup).
    """
    doc = fitz.open(stream=content, filetype="pdf")
    limit = min(n_pages, doc.page_count)
    return "\n".join(doc[i].get_text() for i in range(limit))


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


def pdf_to_md_cascading(content) -> str:
    """Convert PDF bytes to markdown, preferring olmocr and falling back to pymupdf4llm.

    olmocr generally produces higher-fidelity markdown (especially for OCR-heavy
    PDFs) but requires the CLI to be installed; pymupdf4llm is always available.
    """
    from .olmocr import is_olmocr_available, pdf_to_md_str_olmocr

    if is_olmocr_available():
        try:
            md = pdf_to_md_str_olmocr(content)
            if md.strip():
                return md
            print("DEBUG: olmocr returned empty markdown, falling back to pymupdf4llm")
        except Exception as e:
            print(f"DEBUG: olmocr failed ({e}), falling back to pymupdf4llm")

    return pdf_to_md_str(content)


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
