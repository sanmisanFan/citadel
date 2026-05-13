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


def _extract_numeric_label(text: str | None) -> int | None:
    """Extract a numeric citation label from TEI text like "7" or "[7]"."""
    if not text:
        return None
    stripped = text.strip()
    match = re.fullmatch(r"\[?(\d+)\]?", stripped)
    if match:
        return int(match.group(1))
    return None


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
        label_elem = bibl.find("tei:label", TEI_NS)
        label_ref_id = _extract_numeric_label(
            label_elem.text if label_elem is not None else None
        )
        ref = parse_single_bibl_struct(bibl, label_ref_id or idx)
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


def extract_citation_mentions_with_grobid(pdf_content: bytes) -> dict[int, list[dict]]:
    """
    Extract citation mentions (in-text citations) from PDF using grobid.

    This uses the fulltext endpoint which provides citation context.

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        Dictionary mapping reference numbers to list of {text, page} dicts
    """
    url = f"{GROBID_URL}/api/processFulltextDocument"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            data={"consolidateCitations": "0", "teiCoordinates": ["ref", "p"]},
            timeout=GROBID_TIMEOUT,
        )

        if response.status_code != 200:
            return {}

        return parse_citation_mentions(response.text)

    except requests.RequestException:
        return {}


def _parse_coord_boxes(coords: str) -> list[dict]:
    """Parse a TEI ``coords`` attribute into a list of boxes.

    Coords format: ``"page,x,y,width,height;..."`` — a semicolon-separated
    list of one or more boxes. Returns an empty list when no parseable box
    is found.
    """
    if not coords:
        return []
    boxes: list[dict] = []
    for chunk in coords.split(";"):
        parts = chunk.strip().split(",")
        if len(parts) < 5 or not parts[0].isdigit():
            continue
        try:
            boxes.append(
                {
                    "page": int(parts[0]),
                    "x": float(parts[1]),
                    "y": float(parts[2]),
                    "width": float(parts[3]),
                    "height": float(parts[4]),
                }
            )
        except ValueError:
            continue
    return boxes


def _page_from_coords(coords: str) -> int | None:
    """Parse the first page number out of a TEI ``coords`` attribute.

    Coords format: ``"page,x,y,width,height;..."`` (may contain multiple
    boxes separated by ``;``). Returns ``None`` when no valid page is found.
    """
    boxes = _parse_coord_boxes(coords)
    return boxes[0]["page"] if boxes else None


def _parse_page_dimensions(root: ET.Element) -> dict[int, dict]:
    """Read TEI ``<surface>`` elements to learn each page's pixel dimensions.

    Returns ``{page_num: {"width": float, "height": float}}``. Missing
    surfaces default to US-Letter at 72 DPI on the frontend side; callers
    should treat a missing entry as "unknown" rather than zero.
    """
    dims: dict[int, dict] = {}
    for surface in root.findall(".//tei:surface", TEI_NS):
        try:
            page_num = int(surface.get("n", ""))
        except ValueError:
            continue
        try:
            width = float(surface.get("lrx", "0")) - float(surface.get("ulx", "0"))
            height = float(surface.get("lry", "0")) - float(surface.get("uly", "0"))
        except ValueError:
            continue
        if width > 0 and height > 0:
            dims[page_num] = {"width": width, "height": height}
    return dims


def _flatten_paragraph(elem: ET.Element):
    """Walk an element in document order, yielding (kind, payload) tuples.

    Each yield is either ``("text", str)`` for character data or
    ``("ref", ref_elem)`` for a citation marker. The concatenation of all
    text payloads with the ref labels embedded equals ``"".join(elem.itertext())``.
    """
    if elem.text:
        yield ("text", elem.text)
    for child in elem:
        tag = child.tag.split("}", 1)[-1]
        if tag == "ref" and child.get("type") == "bibr":
            label = "".join(child.itertext())
            yield ("ref", child, label)
        else:
            yield from _flatten_paragraph(child)
        if child.tail:
            yield ("text", child.tail)


def parse_citation_mentions(tei_xml: str) -> dict[int, list[dict]]:
    """
    Parse grobid fulltext TEI XML to extract per-citation marker info.

    For each reference number, returns a list of mention records, one per
    paragraph that cites the reference. Each mention exposes:

    - ``text``: the full paragraph text (kept identical to the old shape so
      ``gpt_relevance`` can still key its assessment lookup on it),
    - ``page``: page of the first occurrence of this ref in this paragraph,
    - ``occurrences``: a list of every ``[N]`` marker inside ``text`` for
      this ref, each with ``page``, ``marker_bbox`` (in TEI page coords),
      ``ref_label``, ``char_offset`` (into ``text``), and ``page_width`` /
      ``page_height`` for downstream normalization.

    Args:
        tei_xml: TEI XML string from grobid fulltext endpoint

    Returns:
        Dictionary mapping reference numbers to list of mention records.
    """
    mentions: dict[int, list[dict]] = {}

    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError:
        return {}

    page_dims = _parse_page_dimensions(root)

    # Walk every paragraph; for each <ref type="bibr"> inside, compute the
    # character offset into the paragraph text and harvest the bbox. We do
    # this paragraph-by-paragraph rather than ref-by-ref so we don't pay
    # O(n) parent-pointer lookups for every marker.
    for paragraph in root.findall(".//tei:p", TEI_NS):
        # Build paragraph text and per-ref offsets in one pass.
        pieces: list[str] = []
        cursor = 0
        ref_records: list[tuple[ET.Element, str, int]] = []  # (ref_elem, label, offset)
        for item in _flatten_paragraph(paragraph):
            if item[0] == "text":
                pieces.append(item[1])
                cursor += len(item[1])
            elif item[0] == "ref":
                _, ref_elem, label = item
                ref_records.append((ref_elem, label, cursor))
                pieces.append(label)
                cursor += len(label)

        raw_text = "".join(pieces)
        # Match the pre-existing paragraph text shape: stripped of leading /
        # trailing whitespace. Shift each offset by the count of leading
        # whitespace we strip so offsets remain valid against ``text``.
        leading = len(raw_text) - len(raw_text.lstrip())
        text = raw_text.strip()
        if not text or not ref_records:
            continue

        paragraph_page = _page_from_coords(paragraph.get("coords", ""))

        # Group ref occurrences by ref_num so a single paragraph that cites
        # the same ref twice produces one mention with two occurrences.
        per_ref: dict[int, list[dict]] = {}
        for ref_elem, label, offset in ref_records:
            ref_num = _extract_numeric_label(label)
            if ref_num is None:
                target = ref_elem.get("target", "")
                m = re.match(r"#b(\d+)", target)
                if m:
                    ref_num = int(m.group(1)) + 1
            if ref_num is None:
                continue

            boxes = _parse_coord_boxes(ref_elem.get("coords", ""))
            # Use the first box as the primary anchor; record the rest so
            # the frontend can render wrapping markers (rare).
            if not boxes:
                # Fall back to paragraph page with no bbox — frontend will
                # use the sentence fallback for this marker.
                boxes = [
                    {
                        "page": paragraph_page if paragraph_page is not None else 1,
                        "x": None,
                        "y": None,
                        "width": None,
                        "height": None,
                    }
                ]

            primary = boxes[0]
            page_num = primary["page"]
            dims = page_dims.get(page_num, {})
            occurrence = {
                "page": page_num,
                "marker_bbox": (
                    None
                    if primary.get("x") is None
                    else {
                        "x": primary["x"],
                        "y": primary["y"],
                        "width": primary["width"],
                        "height": primary["height"],
                    }
                ),
                "ref_label": label.strip() or f"[{ref_num}]",
                "char_offset": max(offset - leading, 0),
                "page_width": dims.get("width"),
                "page_height": dims.get("height"),
            }
            per_ref.setdefault(ref_num, []).append(occurrence)

        for ref_num, occurrences in per_ref.items():
            mentions.setdefault(ref_num, [])
            # De-duplicate paragraphs we've already recorded for this ref —
            # grobid sometimes emits the same paragraph twice when it
            # straddles a column break.
            if any(m["text"] == text for m in mentions[ref_num]):
                continue
            mentions[ref_num].append(
                {
                    "text": text,
                    "page": occurrences[0]["page"],
                    "occurrences": occurrences,
                }
            )

    return mentions


def extract_formula_coordinates_with_grobid(pdf_content: bytes) -> list[dict]:
    """
    Extract formula/equation coordinates from PDF using grobid.
    This includes statistical test notations like F(2,46) = 4, p < .01

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        List of dicts with 'text', 'page', 'x', 'y', 'width', 'height'
    """
    url = f"{GROBID_URL}/api/processFulltextDocument"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            data={
                "teiCoordinates": ["formula", "ref", "p"],
                "includeRawAffiliations": "0",
            },
            timeout=GROBID_TIMEOUT,
        )

        if response.status_code != 200:
            print(
                f"DEBUG grobid: Formula extraction failed with status {response.status_code}"
            )
            return []

        return parse_formula_coordinates(response.text)

    except requests.RequestException as e:
        print(f"DEBUG grobid: Formula extraction request failed: {e}")
        return []


def parse_formula_coordinates(tei_xml: str) -> list[dict]:
    """
    Parse grobid TEI XML to extract formula coordinates.

    Args:
        tei_xml: TEI XML string from grobid fulltext endpoint

    Returns:
        List of dicts with formula text and coordinates
    """
    formulas = []

    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError as e:
        print(f"DEBUG grobid: Failed to parse formula XML: {e}")
        return []

    # Find all formula elements with coordinates
    for formula in root.findall(".//tei:formula[@coords]", TEI_NS):
        coords_str = formula.get("coords", "")
        text = "".join(formula.itertext()).strip()

        if not coords_str or not text:
            continue

        # Parse coordinates: "page,x,y,width,height" (can have multiple boxes separated by ;)
        for coord_part in coords_str.split(";"):
            parts = coord_part.strip().split(",")
            if len(parts) >= 5:
                try:
                    formulas.append(
                        {
                            "text": text,
                            "page": int(parts[0]),
                            "x": float(parts[1]),
                            "y": float(parts[2]),
                            "width": float(parts[3]),
                            "height": float(parts[4]),
                        }
                    )
                except (ValueError, IndexError) as e:
                    print(f"DEBUG grobid: Failed to parse coords '{coord_part}': {e}")
                    continue

    # Also look for inline formulas in paragraphs
    for p in root.findall(".//tei:p", TEI_NS):
        p_coords = p.get("coords", "")
        p_text = "".join(p.itertext()).strip()

        # Check if paragraph contains statistical test patterns
        import re

        stat_patterns = [
            r"[FfTt]\s*\([^)]+\)\s*=\s*[\d.]+\s*,?\s*[pP]\s*[<>=]\s*[\d.]+",
            r"[χXx]\s*[²2]?\s*\([^)]+\)\s*=\s*[\d.]+\s*,?\s*[pP]\s*[<>=]\s*[\d.]+",
        ]

        for pattern in stat_patterns:
            for match in re.finditer(pattern, p_text):
                if p_coords:
                    # Use paragraph coordinates as approximation
                    for coord_part in p_coords.split(";"):
                        parts = coord_part.strip().split(",")
                        if len(parts) >= 5:
                            try:
                                formulas.append(
                                    {
                                        "text": match.group(0),
                                        "page": int(parts[0]),
                                        "x": float(parts[1]),
                                        "y": float(parts[2]),
                                        "width": float(parts[3]),
                                        "height": float(parts[4]),
                                        "is_paragraph_coords": True,  # Flag that these are paragraph-level coords
                                    }
                                )
                            except (ValueError, IndexError):
                                continue

    print(f"DEBUG grobid: Found {len(formulas)} formula coordinates")
    return formulas


def extract_abstract_with_grobid(pdf_content: bytes) -> dict | None:
    """
    Extract abstract and header info from a PDF using GROBID.

    Uses the processHeaderDocument endpoint which extracts:
    - Title
    - Authors
    - Abstract
    - Affiliations

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        Dict with 'title', 'authors', 'abstract' or None if extraction fails
    """
    url = f"{GROBID_URL}/api/processHeaderDocument"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            timeout=GROBID_TIMEOUT,
        )

        print(f"DEBUG grobid: Header extraction status: {response.status_code}")
        print(
            f"DEBUG grobid: Response content type: {response.headers.get('content-type', 'unknown')}"
        )
        print(f"DEBUG grobid: Response length: {len(response.text)} chars")
        print(
            f"DEBUG grobid: Response preview: {response.text[:500] if response.text else 'EMPTY'}"
        )

        if response.status_code == 204:
            print("DEBUG grobid: No content returned (204)")
            return None

        if response.status_code != 200:
            print(
                f"DEBUG grobid: Header extraction failed with status {response.status_code}"
            )
            print(f"DEBUG grobid: Error response: {response.text[:500]}")
            return None

        # Check if response looks like XML
        if (
            not response.text
            or not response.text.strip().startswith("<?xml")
            and not response.text.strip().startswith("<")
        ):
            print(f"DEBUG grobid: Response is not XML: {response.text[:200]}")
            print("DEBUG grobid: Trying fulltext endpoint as fallback...")
            return extract_abstract_with_fulltext(pdf_content)

        result = parse_header_tei(response.text)

        # If header parsing failed or no abstract, try fulltext
        if result is None or not result.get("abstract"):
            print("DEBUG grobid: Header extraction incomplete, trying fulltext...")
            return extract_abstract_with_fulltext(pdf_content)

        return result

    except requests.RequestException as e:
        print(f"DEBUG grobid: Header extraction request failed: {e}")
        # Try fulltext as fallback
        print("DEBUG grobid: Trying fulltext endpoint as fallback...")
        return extract_abstract_with_fulltext(pdf_content)


def parse_header_tei(tei_xml: str) -> dict | None:
    """
    Parse GROBID TEI XML header output to extract abstract.

    Args:
        tei_xml: TEI XML string from GROBID processHeaderDocument

    Returns:
        Dict with 'title', 'authors', 'abstract' or None
    """
    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError as e:
        print(f"DEBUG grobid: Failed to parse header XML: {e}")
        return None

    result = {
        "title": None,
        "authors": [],
        "abstract": None,
    }

    # Extract title - try multiple paths
    title_elem = root.find(".//tei:titleStmt/tei:title", TEI_NS)
    if title_elem is None:
        title_elem = root.find(".//tei:title[@type='main']", TEI_NS)
    if title_elem is None:
        title_elem = root.find(".//tei:title", TEI_NS)
    if title_elem is not None:
        result["title"] = "".join(title_elem.itertext()).strip()

    # Extract authors
    for author in root.findall(".//tei:sourceDesc//tei:author", TEI_NS):
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
                result["authors"].append(" ".join(name_parts))

    # Extract abstract - try multiple paths
    abstract_elem = root.find(".//tei:profileDesc/tei:abstract", TEI_NS)
    if abstract_elem is None:
        abstract_elem = root.find(".//tei:abstract", TEI_NS)

    if abstract_elem is not None:
        # Get all text content from the abstract element (may have nested <p> tags)
        abstract_text = "".join(abstract_elem.itertext()).strip()
        if abstract_text:
            result["abstract"] = abstract_text

    # Check if we got an abstract
    if result["abstract"]:
        print(f"DEBUG grobid: Extracted abstract ({len(result['abstract'])} chars)")
        return result
    else:
        print("DEBUG grobid: No abstract found in header")
        return None


def extract_abstract_with_fulltext(pdf_content: bytes) -> dict | None:
    """
    Extract abstract using GROBID's fulltext endpoint as fallback.
    This processes the entire document which is slower but more robust.

    Args:
        pdf_content: Raw PDF file bytes

    Returns:
        Dict with 'title', 'authors', 'abstract' or None
    """
    url = f"{GROBID_URL}/api/processFulltextDocument"

    try:
        response = requests.post(
            url,
            files={"input": ("paper.pdf", pdf_content, "application/pdf")},
            data={"consolidateHeader": "1"},
            timeout=GROBID_TIMEOUT,
        )

        if response.status_code != 200:
            print(
                f"DEBUG grobid: Fulltext extraction failed with status {response.status_code}"
            )
            return None

        # Parse the fulltext TEI - abstract is in the same location
        return parse_header_tei(response.text)

    except requests.RequestException as e:
        print(f"DEBUG grobid: Fulltext extraction request failed: {e}")
        return None
