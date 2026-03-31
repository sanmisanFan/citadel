from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    File,
    UploadFile,
    Form,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .data.utils import pdf_to_md_str
from .data.raw_ref_to_json import PaperProcessor
from .data.process_references import process_markdown_string, parse_references
from .anomalies.gpt_relevance import (
    process_citation_mentions,
    assign_scores_to_enriched_papers,
)
from .anomalies.author_sus import build_suspicious_authors_graph
from .anomalies.detect_anomalies import find_anomalies
from .anomalies.venue_sus import detect_suspicious_venues
from .anomalies.stat_check import generate_statistical_anomalies

from .data.citation_graph_builder import extract_info, build_author_graph
from .data.grobid import (
    is_grobid_available,
    extract_references_with_grobid,
    extract_citation_mentions_with_grobid,
    extract_formula_coordinates_with_grobid,
    extract_abstract_with_grobid,
)
from openai import OpenAI

import os
import sys
import asyncio
import json
from pathlib import Path
from time import time

# =============================================================================
# DEBUGGING: Output directory for debug files
# =============================================================================
DEBUG_OUTPUT_DIR = Path("outputs/debug")

# =============================================================================
# DEBUGGING: Pipeline step tracker for API call monitoring
# Tracks duration and details for each pipeline step
# =============================================================================
class PipelineTracker:
    """DEBUGGING: Tracks pipeline steps, durations, and API call counts."""
    def __init__(self):
        self.steps = []
        self.start_time = time()

    def record(self, step_name: str, duration: float, details: dict = None):
        """DEBUGGING: Record a pipeline step with timing and optional details."""
        self.steps.append({
            "step": step_name,
            "duration_seconds": round(duration, 2),
            "details": details or {}
        })

    def get_summary(self):
        """DEBUGGING: Get summary of all pipeline steps."""
        return {
            "total_time_seconds": round(time() - self.start_time, 2),
            "steps": self.steps
        }

# DEBUGGING: Global tracker instance
pipeline_tracker = None


# =============================================================================
# DEBUGGING: Save all pipeline outputs to JSON files for inspection
# =============================================================================
def save_debug_outputs(
    enriched_papers,
    citations,
    authors,
    venues,
    anomalous_data,
    author_graph,
    reference_mentions,
    tracker_summary=None,
):
    """DEBUGGING: Save all pipeline outputs to JSON files for debugging."""
    DEBUG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "enriched_papers.json": enriched_papers,
        "citations.json": list(citations.values()) if isinstance(citations, dict) else citations,
        "authors.json": authors,
        "venues.json": venues,
        "anomalous.json": anomalous_data,
        "author_graph.json": author_graph,
        "reference_mentions.json": reference_mentions,
    }

    # DEBUGGING: Save markdown text for stat check inspection
    if tracker_summary and "md_text" in tracker_summary:
        md_filepath = DEBUG_OUTPUT_DIR / "paper_markdown.md"
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(tracker_summary["md_text"])
        print(f"DEBUG: Saved {md_filepath}")

    # DEBUGGING: Add pipeline tracking summary if available
    if tracker_summary:
        outputs["pipeline_summary.json"] = tracker_summary

    for filename, data in outputs.items():
        filepath = DEBUG_OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"DEBUG: Saved {filepath}")

    print(f"DEBUG: All outputs saved to {DEBUG_OUTPUT_DIR}/")


def extract_references_grobid_with_fallback(
    pdf_content: bytes,
    gpt_client,
    progress_fn,
):
    """
    Extract references using grobid if available, otherwise fall back to
    markdown parsing + GPT.

    Args:
        pdf_content: Raw PDF bytes
        gpt_client: OpenAI client for GPT parsing fallback
        progress_fn: Function to report progress

    Returns:
        Tuple of (parsed_references, reference_mentions, md_text or None)
    """
    use_grobid = is_grobid_available()
    md_text = None  # Only create markdown if needed

    if use_grobid:
        progress_fn("info", "Extracting references with grobid...")
        try:
            parsed_refs, raw_refs = extract_references_with_grobid(pdf_content)
            if parsed_refs:
                print(f"DEBUG: Grobid extracted {len(parsed_refs)} references")

                # Try to get citation mentions from grobid fulltext
                reference_mentions = extract_citation_mentions_with_grobid(pdf_content)

                # If grobid didn't get good citation context, fall back to markdown parsing
                if not reference_mentions:
                    print("DEBUG: Grobid citation mentions empty, trying markdown fallback")
                    progress_fn("info", "Converting PDF to markdown for citation mentions...")
                    try:
                        md_text = pdf_to_md_str(pdf_content)
                        reference_mentions, _ = process_markdown_string(md_text)
                    except ValueError as e:
                        print(f"DEBUG: Markdown fallback failed: {e}")
                        print("DEBUG: Proceeding with empty citation mentions")
                        reference_mentions = {}

                return parsed_refs, reference_mentions, md_text
            else:
                print("DEBUG: Grobid returned no references, falling back to markdown+GPT")
        except Exception as e:
            print(f"DEBUG: Grobid failed: {e}, falling back to markdown+GPT")

    # Fallback: markdown parsing + GPT
    progress_fn("info", "Converting PDF to markdown...")
    md_text = pdf_to_md_str(pdf_content)

    progress_fn("info", "Extracting references from markdown...")
    try:
        reference_mentions, raw_references = process_markdown_string(md_text)
    except ValueError as e:
        print(f"DEBUG: Could not find references section: {e}")
        progress_fn("info", "References section not found in PDF. The paper may have non-standard formatting.")
        # Return empty results - the pipeline can still proceed
        return [], {}, md_text

    progress_fn("info", "Parsing references with GPT...")
    parsed_refs = parse_references(gpt_client, raw_references)

    return parsed_refs, reference_mentions, md_text

if "OPENAI_API_KEY" not in os.environ:
    print("ERROR: $OPENAI_API_KEY not set!")
    sys.exit(1)

app = FastAPI()

# Add CORS middleware for frontend API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def serve_frontend():
    return {"test"}


@app.websocket("/ws/process_pdf")
async def process_pdf_ws(ws: WebSocket):
    await ws.accept()
    try:
        paper_metadata = await ws.receive_json()
        file_metadata = await ws.receive_json()
        contents = await ws.receive_bytes()

        # debugging: track API calls and timing
        global pipeline_tracker
        pipeline_tracker = PipelineTracker()

        progress_q: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def progress(msg_type: str, msg: str, data: dict | None = None):
            progress_q.put_nowait({"type": msg_type, "msg": msg, "data": data})

        async def sender():
            while True:
                event = await progress_q.get()
                await ws.send_json(event)
                await asyncio.sleep(0)
                if event["type"] == "end":
                    break

        sender_task = asyncio.create_task(sender())
        # TODO: could we ask the user where the references are?
        if file_metadata["mime_type"] != "application/pdf":
            raise WebSocketException(code=1003, reason="Only PDF files are allowed.")

        # TODO: eventually make this a wrapper for other LLMs and expose functions
        # for each type of call the pipeline makes
        if "OPENAI_API_KEY" not in os.environ:
            raise WebSocketException(
                code=1011, reason="Backend did not set OpenAI API key."
            )

        gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # TODO: https://github.com/allenai/olmocr for pdf conversion

        # Try grobid first, fall back to markdown+GPT
        # Markdown is only created if needed (grobid fallback)
        t0 = time()
        parsed, reference_mentions, md_text = await asyncio.to_thread(
            extract_references_grobid_with_fallback,
            contents,
            gpt_client,
            progress,
        )
        pipeline_tracker.record("reference_extraction", time() - t0, {"refs": len(parsed), "mentions": len(reference_mentions)})

        progress("info", "Processing papers...")

        # Enrich parsed references with Semantic Scholar / OpenAlex metadata
        processor = PaperProcessor(gpt_client=gpt_client)

        t0 = time()
        enriched, entity_keys = await asyncio.to_thread(
            processor.process_papers, parsed, reference_mentions
        )
        pipeline_tracker.record("enrichment_s2_openalex", time() - t0, {"papers": len(enriched)})

        progress("info", "Running relevance assessment...")

        t0 = time()
        citation_assessments = await asyncio.to_thread(
            process_citation_mentions, reference_mentions, enriched, gpt_client
        )
        # why not just update this in process_citation_mentions?
        # or better yet, just keep these as separate objects?
        updated_enriched_papers = await asyncio.to_thread(
            assign_scores_to_enriched_papers, enriched, citation_assessments
        )
        pipeline_tracker.record("relevance_assessment_gpt", time() - t0, {"assessments": len(citation_assessments)})

        progress("info", "Building graphs...")

        t0 = time()
        citations, authors, venues = await asyncio.to_thread(
            extract_info, entity_keys, paper_metadata
        )

        # not used?
        suspicious_sccs_g, sus_hop1_sccs, sccs_info = await asyncio.to_thread(
            build_suspicious_authors_graph, authors, citations
        )

        anomalous_data = await asyncio.to_thread(
            find_anomalies, updated_enriched_papers, sus_hop1_sccs, citations
        )
        # not used?
        export_data_suspicious, export_data_hop, scc_details = await asyncio.to_thread(
            detect_suspicious_venues, citations, venues
        )

        ag = await asyncio.to_thread(build_author_graph, citations)

        # Run statistical validation using plain text extracted from PDF
        progress("info", "Checking statistical tests...")

        # DEBUG: Extract plain text and check what statistical tests are found
        from .anomalies.stat_check import find_all_tests, pdf_to_plain_text, preprocess_text
        DEBUG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        plain_text = pdf_to_plain_text(contents)
        preprocessed_text = preprocess_text(plain_text)

        # Save plain text for debugging
        plain_debug_path = DEBUG_OUTPUT_DIR / "paper_plain_text.txt"
        with open(plain_debug_path, "w", encoding="utf-8") as f:
            f.write(preprocessed_text)
        print(f"DEBUG: Saved plain text to {plain_debug_path}")

        found_tests = find_all_tests(preprocessed_text)
        print(f"DEBUG: Statistical tests found in plain text:")
        print(f"  F-tests: {found_tests['f_tests']}")
        print(f"  t-tests: {found_tests['t_tests']}")
        print(f"  chi-square: {found_tests['chi_square_tests']}")

        # Extract formula coordinates from GROBID for precise highlighting
        formula_coords = None
        if is_grobid_available():
            print("DEBUG: Extracting formula coordinates from GROBID...")
            formula_coords = await asyncio.to_thread(
                extract_formula_coordinates_with_grobid, contents
            )
            print(f"DEBUG: Found {len(formula_coords) if formula_coords else 0} formula coordinates from GROBID")
            # Save formula coords for debugging
            if formula_coords:
                formula_coords_path = DEBUG_OUTPUT_DIR / "formula_coords.json"
                with open(formula_coords_path, "w", encoding="utf-8") as f:
                    json.dump(formula_coords, f, indent=2)
                print(f"DEBUG: Saved formula coords to {formula_coords_path}")
        else:
            print("DEBUG: GROBID not available, skipping formula coordinate extraction")

        stat_anomalies = await asyncio.to_thread(
            generate_statistical_anomalies, contents, len(anomalous_data.get("identifiedIssue", [])) + 1,
            0.01, formula_coords
        )
        anomalous_data["identifiedIssue"].extend(stat_anomalies)
        print(f"DEBUG: Found {len(stat_anomalies)} statistical anomalies")

        # Set has_issue and id on citations based on anomalies
        anomalous_citation_keys = set()
        for issue in anomalous_data.get("identifiedIssue", []):
            for paper_key in issue.get("paper", []):
                anomalous_citation_keys.add(paper_key)

        for citation_key, citation in citations.items():
            citation["id"] = citation_key  # Add id field for frontend compatibility
            citation["has_issue"] = citation_key in anomalous_citation_keys

        pipeline_tracker.record("build_graphs_and_anomalies", time() - t0, {"anomalies": len(anomalous_data.get("identifiedIssue", []))})

        # debugging: save debug outputs including pipeline summary
        await asyncio.to_thread(
            save_debug_outputs,
            updated_enriched_papers,
            citations,
            authors,
            venues,
            anomalous_data,
            ag,
            reference_mentions,
            pipeline_tracker.get_summary(),
        )

        await progress_q.put(
            {
                "type": "end",
                "results": {
                    "authors": authors,
                    "venues": venues,
                    "citations": list(citations.values()),
                    "anomalous": anomalous_data,
                    "authorGraph": ag,
                },
            }
        )
        await sender_task

    except WebSocketDisconnect:
        print("Disconnected.")


@app.post("/api/extract_abstract")
async def extract_abstract_from_pdf(
    file: UploadFile = File(...),
    citation_id: str = Form(...),
):
    """
    Extract abstract from a PDF file using GROBID.
    Used when a referenced paper is missing its abstract.

    Args:
        file: PDF file upload
        citation_id: ID of the citation to update

    Returns:
        Dict with citation_id, abstract, title, authors
    """
    if not is_grobid_available():
        raise HTTPException(
            status_code=503,
            detail="GROBID service is not available. Please start GROBID first."
        )

    contents = await file.read()

    result = await asyncio.to_thread(extract_abstract_with_grobid, contents)

    if result is None:
        raise HTTPException(
            status_code=422,
            detail="Could not extract abstract from PDF. The PDF may not have an abstract section."
        )

    return {
        "citation_id": citation_id,
        "abstract": result.get("abstract"),
        "title": result.get("title"),
        "authors": result.get("authors", []),
    }


@app.post("/api/extract_abstracts")
async def extract_abstracts_batch(
    files: list[UploadFile] = File(...),
    citation_ids: str = Form(...),  # Comma-separated citation IDs
):
    """
    Extract abstracts from multiple PDFs using GROBID.
    Accepts multipart form data with multiple files and comma-separated citation IDs.

    Args:
        files: List of PDF file uploads
        citation_ids: Comma-separated citation IDs matching the files order

    Returns:
        Dict with results for each citation
    """
    if not is_grobid_available():
        raise HTTPException(
            status_code=503,
            detail="GROBID service is not available. Please start GROBID first."
        )

    ids = citation_ids.split(",")

    if len(files) != len(ids):
        raise HTTPException(
            status_code=400,
            detail=f"Number of files ({len(files)}) doesn't match number of citation IDs ({len(ids)})"
        )

    results = []

    for file, cid in zip(files, ids):
        contents = await file.read()
        print(f"DEBUG: Processing file '{file.filename}' ({len(contents)} bytes) for citation {cid}")

        if len(contents) == 0:
            print(f"DEBUG: Warning - file '{file.filename}' is empty!")
            results.append({
                "citation_id": cid.strip(),
                "abstract": None,
                "success": False,
                "error": "Empty file received",
            })
            continue

        result = await asyncio.to_thread(extract_abstract_with_grobid, contents)

        if result and result.get("abstract"):
            results.append({
                "citation_id": cid.strip(),
                "abstract": result.get("abstract"),
                "title": result.get("title"),
                "authors": result.get("authors", []),
                "success": True,
            })
        else:
            results.append({
                "citation_id": cid.strip(),
                "abstract": None,
                "success": False,
                "error": "Could not extract abstract from PDF",
            })

    return {
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }
