from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .lib import pdf_to_md_str
from .process_references import process_markdown_string
import os
import sys

if "OPENAI_API_KEY" not in os.environ:
    print("ERROR: $OPENAI_API_KEY not set!")
    sys.exit(1)

app = FastAPI()


@app.get("/")
def serve_frontend():
    return {"test"}


@app.post("/process_pdf")
async def process_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    contents = await file.read()

    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400, detail="Uploaded file does not appear to be a valid PDF."
        )

    # following pipeline from backend_scripts
    md_text = pdf_to_md_str(contents)  # convert pdf to md
    reference_mentions, raw_references = process_markdown_string(
        md_text
    )  # get references
