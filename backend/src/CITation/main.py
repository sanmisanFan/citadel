from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .data.utils import pdf_to_md_str
from .data.raw_ref_to_json import PaperProcessor
from .data.process_references import process_markdown_string
from .anomalies.gpt_relevance import (
    process_citation_mentions,
    assign_scores_to_enriched_papers,
)
from .data.citation_graph_builder import extract_info
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


# TODO: update with additional papermetadata
@app.post("/process_pdf")
async def process_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    contents = await file.read()

    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400, detail="Uploaded file does not appear to be a valid PDF."
        )

    # TODO: eventually make this a wrapper for other LLMs and expose functions
    # for each type of call the pipeline makes
    if "OPENAI_API_KEY" not in os.environ:
        raise HTTPException(
            status_code=500, detail="Backend did not set OpenAI API key."
        )

    gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # TODO: https://github.com/allenai/olmocr for pdf conversion
    # following pipeline from backend_scripts
    md_text = pdf_to_md_str(contents)  # convert pdf to md
    reference_mentions, raw_references = process_markdown_string(
        md_text
    )  # get references
    processor = PaperProcessor(gpt_client)
    enriched, entity_keys = processor.process_papers(raw_references, reference_mentions)
    citation_assessments = process_citation_mentions(
        reference_mentions, enriched, gpt_client
    )
    # why not just update this in process_citation_mentions?
    # or better yet, just keep these as separate objects?
    updated_enriched_papers = assign_scores_to_enriched_papers(
        enriched, citation_assessments
    )

    # need to read from user
    p_md = {}

    # so in the end we have the "enriched" paper data and the entity_keys list -
    # the entity keys list contains
    # authors - who all have a unique ID assigned to them, plus their names and orcids
    # venues, who all have a unique venue ID assigned
    # citations - a list of all of the references, 1st and second hop included... this data contains a lot of duplicate
    # information
    # enriched is the same as citations, but only contains the one hop references
    # papers that were directly referenced in the paper being analyzed have additional info, like where in the text they were
    # mentioned, and a relevance score. they also contain a list of all of the references for this paper
    citations, authors, venues = extract_info(
        updated_enriched_papers, entity_keys, p_md
    )
