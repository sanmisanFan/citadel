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

    """
### 3. `raw_ref_to_json.py`
  - `outputs/rawreferences.txt`
  - `outputs/reference_mentions.json`
- **Output**:
  - `outputs/enriched_papers.json`
  - `outputs/entity_keys.json`
- **Run**:
  ```bash
  python raw_ref_to_json.py
  ```

### 4. `summarize.py`

- Summarizes referenced papers using GPT.
- **Input**: `reference_papers/*.pdf`
- **Output**: `outputs/pdf_summaries.json`
- **Run**:
  ```bash
  python summarize.py
  ```

### 5. `gpt_relevance.py`

- Uses GPT to score citation relevance.
- **Input**:
  - `outputs/reference_mentions.json`
  - `outputs/pdf_summaries.json`
  - `outputs/enriched_papers.json`
- **Output**:
  - `outputs/detailed_citation_assessments.json`
  - `outputs/enriched_papers_with_scores.json`
- **Run**:
  ```bash
  python gpt_relevance.py
  ```

### 6. `cit_locator.py`

- Locates and annotates citation mentions in the original PDF.
- **Input**:
  - `test.pdf`
  - `outputs/enriched_papers_with_scores.json`
- **Output**:
  - `outputs/annotated_test.pdf`
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/annotated_results.json`
- **Run**:
  ```bash
  python cit_locator.py
  ```

### 7. `second_hop.py`

- Fetches second-hop citations and updates the graph.
- **Input**:
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/second_hop_references.json`
  - Updates `outputs/entity_keys.json`
- **Run**:
  ```bash
  python second_hop.py
  ```

### 8. `citation_graph_builder.py`

- Builds final citation, author, and venue graphs.
- **Input**:
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/second_hop_references.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/citations.json`
  - `outputs/authors.json`
  - `outputs/venues.json`
- **Run**:
  ```bash
  python citation_graph_builder.py
  ```

### 9. `paper_details.py`

- Adds the primary paper (hop=0) into the citation, author, and venue graphs.
- **Input**:
  - `outputs/citations.json`
  - `outputs/authors.json`
  - `outputs/venues.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/citations_updated.json`
  - `outputs/authors_updated.json`
  - `outputs/venues_updated.json`
  - `outputs/entity_keys_updated.json`
- **Run**:
  ```bash
  python paper_details.py
  ```
- Note: Creates `citation-0` for the main paper and links all hop-1 references to it.

### 10. `generate_anomalous_json.py`

- Detects citation anomalies based on low relevance scores and potential author manipulation via SCCs.
- **Input**:
  - `outputs/enriched_papers_with_scores.json`
  - `outputs/suspicious_hop1_only_sccs.json`
  - `outputs/citations_updated.json`
- **Output**:
  - `outputs/anomalous.json`
- **Run**:
  ```bash
  python generate_anomalous_json.py
  ```
- Note: Flags low-relevancy citations and adds `selfCitation` / `citationRing` indicators if authors belong to hop-1 SCCs.

### 11. `author.sus`

- Identifies suspicious citation rings among authors by analyzing author-author graphs.
- **Input**:
  - `outputs/authors_updated.json`
  - `outputs/citations_updated.json`
- **Output**:
  - `outputs/suspicious_sccs.json`
  - `outputs/suspicious_hop1_only_sccs.json`
  - `outputs/scc_details_with_hop1.json`
- **Run**:
  ```bash
  python author_sus.py
  ```
- Note: Highlights strongly connected components of authors with suspicious citation behaviors, especially if at least one is from hop-1.

### 12. `venue.sus`

- Identifies suspicious venue-level citation clusters based on citation weight and hop status.
- **Input**:
  - `outputs/citations_updated.json`
  - `outputs/venues_updated.json`
- **Output**:
  - `outputs/suspicious_venues.json`
  - `outputs/hop_venues_any.json`
  - `outputs/scc_details_with_hop_any.json`
- **Run**:
  ```bash
  python venue.sus
  ```
- Note: Detects venue-level SCCs where citations suggest manipulation, based on edge weight and inclusion of hop-0 or hop-1 venues.

"""
