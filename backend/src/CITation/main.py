from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
)
from fastapi.responses import JSONResponse
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

from .data.citation_graph_builder import extract_info, build_author_graph
from .data.grobid import (
    is_grobid_available,
    extract_references_with_grobid,
    extract_citation_mentions_with_grobid,
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
    md_text: str,
    gpt_client,
    progress_fn,
):
    """
    Extract references using grobid if available, otherwise fall back to
    markdown parsing + GPT.

    Args:
        pdf_content: Raw PDF bytes
        md_text: Markdown text (used for fallback and citation mentions)
        gpt_client: OpenAI client for GPT parsing fallback
        progress_fn: Function to report progress

    Returns:
        Tuple of (parsed_references, reference_mentions)
    """
    use_grobid = is_grobid_available()

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
                    print("DEBUG: Grobid citation mentions empty, using markdown fallback")
                    reference_mentions, _ = process_markdown_string(md_text)

                return parsed_refs, reference_mentions
            else:
                print("DEBUG: Grobid returned no references, falling back to markdown+GPT")
        except Exception as e:
            print(f"DEBUG: Grobid failed: {e}, falling back to markdown+GPT")

    # Fallback: markdown parsing + GPT
    progress_fn("info", "Extracting references from markdown...")
    reference_mentions, raw_references = process_markdown_string(md_text)

    progress_fn("info", "Parsing references with GPT...")
    parsed_refs = parse_references(gpt_client, raw_references)

    return parsed_refs, reference_mentions

if "OPENAI_API_KEY" not in os.environ:
    print("ERROR: $OPENAI_API_KEY not set!")
    sys.exit(1)

app = FastAPI()


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

        # ugly, but forces fastapi to send the messages
        progress("info", "Converting pdf to markdown...")
        t0 = time()
        md_text = await asyncio.to_thread(pdf_to_md_str, contents)
        pipeline_tracker.record("pdf_to_markdown", time() - t0)

        # Try grobid first, fall back to markdown+GPT
        t0 = time()
        parsed, reference_mentions = await asyncio.to_thread(
            extract_references_grobid_with_fallback,
            contents,
            md_text,
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
