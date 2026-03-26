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
from openai import OpenAI

import os
import sys
import asyncio

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
        md_text = await asyncio.to_thread(pdf_to_md_str, contents)

        # TODO: try https://github.com/grobidOrg/grobid to extract reference metadata
        progress("info", "Extracting references...")
        reference_mentions, raw_references = await asyncio.to_thread(
            process_markdown_string, md_text
        )

        progress("info", "Processing papers...")

        # TODO: figure out how to send messages from process_papers
        processor = PaperProcessor()
        parsed = await asyncio.to_thread(parse_references, gpt_client, raw_references)

        enriched, entity_keys = await asyncio.to_thread(
            processor.process_papers, parsed, reference_mentions
        )

        progress("info", "Running relevance assessment...")

        citation_assessments = await asyncio.to_thread(
            process_citation_mentions, reference_mentions, enriched, gpt_client
        )
        # why not just update this in process_citation_mentions?
        # or better yet, just keep these as separate objects?
        updated_enriched_papers = await asyncio.to_thread(
            assign_scores_to_enriched_papers, enriched, citation_assessments
        )

        progress("info", "Building graphs...")

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
