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
from .data.process_references import process_markdown_string
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

        await ws.send_json({"type": "info", "msg": "Converting pdf to markdown..."})
        md_text = pdf_to_md_str(contents)

        await ws.send_json({"type": "info", "msg": "Extracting references..."})
        reference_mentions, raw_references = process_markdown_string(md_text)

        await ws.send_json({"type": "info", "msg": "Processing papers..."})

        processor = PaperProcessor(gpt_client)
        enriched, entity_keys = processor.process_papers(
            raw_references, reference_mentions
        )

        await ws.send_json({"type": "info", "msg": "Running relevance assessment..."})
        citation_assessments = process_citation_mentions(
            reference_mentions, enriched, gpt_client
        )
        # why not just update this in process_citation_mentions?
        # or better yet, just keep these as separate objects?
        updated_enriched_papers = assign_scores_to_enriched_papers(
            enriched, citation_assessments
        )

        await ws.send_json({"type": "info", "msg": "Building graphs..."})
        citations, authors, venues = extract_info(entity_keys, paper_metadata)

        # not used?
        suspicious_sccs_g, sus_hop1_sccs, sccs_info = build_suspicious_authors_graph(
            authors, citations
        )

        anomalous_data = find_anomalies(
            updated_enriched_papers, sus_hop1_sccs, citations
        )
        # not used?
        export_data_suspicious, export_data_hop, scc_details = detect_suspicious_venues(
            citations, venues
        )

        ag = build_author_graph(citations)

        """
        import authorRaw from "./data/case1/authors.json";
        import venueRaw from "./data/case1/venues.json";
        import citationRaw from "./data/case1/citation.json";
        import anomalousRaw from "./data/case1/anomalous.json";
        import authorGraphDataRaw from "./data/case1/community_graph.json"; # I assume this is from build_author_graph
        """

        result = {
            "authors": authors,
            "venues": venues,
            "citations": citations,
            "anomalous": anomalous_data,
            "authorGraph": ag,
        }
        await ws.send_json({"type": "end", "data": result})

    except WebSocketDisconnect:
        print("Disconnected.")
