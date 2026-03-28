"""
Grobid integration for reference extraction.
Requires a running grobid service (default: localhost:8070).

To run grobid locally via Docker:
    docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0

Set GROBID_URL environment variable to override the default URL.
"""

import os
import re
import requests
import xml.etree.ElementTree as ET
from typing import Tuple
from .datatypes import ParsedReference

GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070")
GROBID_TIMEOUT = 120  # seconds, PDF processing can be slow

# TEI XML namespace
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def is_grobid_available() -> bool:
    """Check if grobid service is running and accessible."""
    try:
        response = requests.get(f"{GROBID_URL}/api/isalive", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def extract_references_with_grobid(
    pdf_content: bytes,
) -> Tuple[list[ParsedReference], list[str]]:
    """
    Extract references from PDF using grobid service.

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        Tuple of (parsed_references, raw_reference_strings)

    Raises:
        RuntimeError: If grobid service fails or is unavailable
    """
    url = f"{GROBID_URL}/api/processReferences"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            data={"consolidateCitations": "1", "includeRawCitations": "1"},
            timeout=GROBID_TIMEOUT,
        )

        if response.status_code == 204:
            # No references found
            return [], []
        elif response.status_code != 200:
            raise RuntimeError(
                f"Grobid returned status {response.status_code}: {response.text}"
            )

        return parse_tei_references(response.text)

    except requests.RequestException as e:
        raise RuntimeError(f"Grobid request failed: {e}")


def parse_tei_references(
    tei_xml: str,
) -> Tuple[list[ParsedReference], list[str]]:
    """
    Parse grobid TEI XML output into structured references.

    Args:
        tei_xml: TEI XML string from grobid

    Returns:
        Tuple of (parsed_references, raw_reference_strings)
    """
    parsed_refs: list[ParsedReference] = []
    raw_refs: list[str] = []

    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError as e:
        print(f"DEBUG: Failed to parse grobid XML: {e}")
        return [], []

    # Find all biblStruct elements (structured references)
    bibl_structs = root.findall(".//tei:biblStruct", TEI_NS)

    for idx, bibl in enumerate(bibl_structs, 1):
        ref = parse_single_bibl_struct(bibl, idx)
        parsed_refs.append(ref)

        # Extract raw citation string if available
        raw_cite = bibl.find(".//tei:note[@type='raw_reference']", TEI_NS)
        if raw_cite is not None and raw_cite.text:
            raw_refs.append(raw_cite.text.strip())
        else:
            # Reconstruct from parsed data
            raw_refs.append(reconstruct_raw_reference(ref))

    return parsed_refs, raw_refs


def parse_single_bibl_struct(bibl: ET.Element, ref_id: int) -> ParsedReference:
    """Parse a single biblStruct element into a ParsedReference."""

    # Extract authors
    authors = []
    for author in bibl.findall(".//tei:author", TEI_NS):
        persname = author.find("tei:persName", TEI_NS)
        if persname is not None:
            forename = persname.find("tei:forename", TEI_NS)
            surname = persname.find("tei:surname", TEI_NS)

            name_parts = []
            if forename is not None and forename.text:
                name_parts.append(forename.text.strip())
            if surname is not None and surname.text:
                name_parts.append(surname.text.strip())

            if name_parts:
                authors.append(" ".join(name_parts))

    # Extract title (article/chapter level first, then monograph level)
    title = None
    for level in ["a", "m"]:
        title_elem = bibl.find(f".//tei:title[@level='{level}']", TEI_NS)
        if title_elem is not None and title_elem.text:
            title = title_elem.text.strip()
            break

    # Extract venue (journal or proceedings)
    venue = None
    raw_venue = None
    # Try journal title first
    journal = bibl.find(".//tei:title[@level='j']", TEI_NS)
    if journal is not None and journal.text:
        venue = journal.text.strip()
        raw_venue = venue
    else:
        # Try monograph title (for proceedings, books)
        monograph = bibl.find(".//tei:title[@level='m']", TEI_NS)
        if monograph is not None and monograph.text and title != monograph.text.strip():
            venue = monograph.text.strip()
            raw_venue = venue

    # Extract year
    year = None
    date_elem = bibl.find(".//tei:date[@when]", TEI_NS)
    if date_elem is not None:
        when = date_elem.get("when", "")
        # Extract just the year (first 4 digits)
        year_match = re.match(r"(\d{4})", when)
        if year_match:
            year = year_match.group(1)
    else:
        # Try date text content
        date_elem = bibl.find(".//tei:date", TEI_NS)
        if date_elem is not None and date_elem.text:
            year_match = re.search(r"(\d{4})", date_elem.text)
            if year_match:
                year = year_match.group(1)

    # Extract pages
    pages = None
    page_from = bibl.find(".//tei:biblScope[@unit='page'][@from]", TEI_NS)
    page_to = bibl.find(".//tei:biblScope[@unit='page'][@to]", TEI_NS)
    if page_from is not None:
        pages = page_from.get("from", "")
        if page_to is not None:
            pages += f"-{page_to.get('to', '')}"
    else:
        page_elem = bibl.find(".//tei:biblScope[@unit='page']", TEI_NS)
        if page_elem is not None and page_elem.text:
            pages = page_elem.text.strip()

    # Extract DOI
    doi = None
    doi_elem = bibl.find(".//tei:idno[@type='DOI']", TEI_NS)
    if doi_elem is not None and doi_elem.text:
        doi = doi_elem.text.strip()
        # Clean up DOI prefix if present
        doi = re.sub(r"^(doi:|https?://doi\.org/)", "", doi, flags=re.IGNORECASE)

    # Extract arXiv ID
    arxiv_id = None
    arxiv_elem = bibl.find(".//tei:idno[@type='arXiv']", TEI_NS)
    if arxiv_elem is not None and arxiv_elem.text:
        arxiv_id = arxiv_elem.text.strip()
        # Clean up arXiv prefix if present
        arxiv_id = re.sub(r"^arXiv:", "", arxiv_id, flags=re.IGNORECASE)

    return ParsedReference(
        authors=authors,
        title=title or "",
        venue=venue,
        raw_venue=raw_venue,
        year=year,
        pages=pages,
        doi=doi,
        arxiv_id=arxiv_id,
        abstract=None,  # Grobid doesn't extract abstracts of cited papers
        ref_id=ref_id,
    )


def reconstruct_raw_reference(ref: ParsedReference) -> str:
    """Reconstruct a raw reference string from parsed data."""
    parts = []

    if ref["authors"]:
        parts.append(", ".join(ref["authors"]))

    if ref["title"]:
        parts.append(f'"{ref["title"]}"')

    if ref["venue"]:
        parts.append(ref["venue"])

    if ref["year"]:
        parts.append(f"({ref['year']})")

    if ref["pages"]:
        parts.append(f"pp. {ref['pages']}")

    if ref["doi"]:
        parts.append(f"doi: {ref['doi']}")

    return ". ".join(parts) if parts else ""


def extract_citation_mentions_with_grobid(pdf_content: bytes) -> dict[int, list[str]]:
    """
    Extract citation mentions (in-text citations) from PDF using grobid.

    This uses the fulltext endpoint which provides citation context.

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        Dictionary mapping reference numbers to list of context sentences
    """
    url = f"{GROBID_URL}/api/processFulltextDocument"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            data={"consolidateCitations": "0", "teiCoordinates": "ref"},
            timeout=GROBID_TIMEOUT,
        )

        if response.status_code != 200:
            return {}

        return parse_citation_mentions(response.text)

    except requests.RequestException:
        return {}


def parse_citation_mentions(tei_xml: str) -> dict[int, list[str]]:
    """
    Parse grobid fulltext TEI XML to extract citation contexts.

    Args:
        tei_xml: TEI XML string from grobid fulltext endpoint

    Returns:
        Dictionary mapping reference numbers to list of context sentences
    """
    mentions: dict[int, list[str]] = {}

    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError:
        return {}

    # Find all ref elements with type="bibr"
    for ref in root.findall(".//tei:ref[@type='bibr']", TEI_NS):
        target = ref.get("target", "")
        # Target format is typically "#b0", "#b1", etc.
        match = re.match(r"#b(\d+)", target)
        if match:
            ref_num = int(match.group(1)) + 1  # Convert 0-indexed to 1-indexed

            # Get the parent paragraph for context
            parent = ref
            context = ""
            for _ in range(5):  # Walk up to 5 levels to find paragraph
                parent = find_parent(root, parent)
                if parent is None:
                    break
                if parent.tag.endswith("}p") or parent.tag == "p":
                    context = "".join(parent.itertext()).strip()
                    break

            if context:
                if ref_num not in mentions:
                    mentions[ref_num] = []
                # Avoid duplicate contexts
                if context not in mentions[ref_num]:
                    mentions[ref_num].append(context)

    return mentions


def find_parent(root: ET.Element, child: ET.Element) -> ET.Element | None:
    """Find parent element in XML tree (ElementTree doesn't have parent pointers)."""
    for parent in root.iter():
        if child in parent:
            return parent
    return None
