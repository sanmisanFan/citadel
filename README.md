# Citadel

Citadel is a research-paper review tool. Upload a PDF and the backend extracts
its references, scores each citation's relevance with an LLM, builds
citation/author/venue graphs, flags anomalies (low-relevance citations,
suspicious author/venue communities, statcheck mismatches), and the frontend
visualizes the results alongside the PDF.

The Python package is `CITation`; the FastAPI app is `CITation.main:app`.

## Architecture

- **Backend** — FastAPI app in [backend/src/CITation/](backend/src/CITation/).
  Exposes a WebSocket (`/ws/process_pdf`) that runs the full pipeline on an
  uploaded PDF, plus REST endpoints for batch abstract extraction. Pipeline
  steps live in [data/](backend/src/CITation/data/) (extraction, enrichment,
  graph building) and [anomalies/](backend/src/CITation/anomalies/) (relevance,
  author/venue suspicion, statcheck).
- **Frontend** — React + Ant Design app in [src/](src/). PDF viewer in
  [src/components/pdfContainer/](src/components/pdfContainer/), graph and
  anomaly visualizations in [src/components/visContainer/](src/components/visContainer/).
- **GROBID** (optional but recommended) — used for reference extraction,
  citation-mention location, formula coordinate extraction (for statcheck
  highlights), and abstract recovery for missing-metadata references.
- **PDF → markdown cascade** — when markdown is needed (GROBID missing or
  unable to locate citation mentions), the backend tries
  [olmocr](https://github.com/allenai/olmocr) first and falls back to
  `pymupdf4llm`. olmocr is not a hard dependency; install it separately if
  you want to use it.

## Prerequisites

- Python ≥ 3.11 with [`uv`](https://docs.astral.sh/uv/)
- Node.js (for the React frontend)
- `OPENAI_API_KEY` set in the environment
- `S2_API_KEY` set in the environment ([Semantic Scholar API key](https://www.semanticscholar.org/product/api))
- Docker (optional, to run GROBID locally)

## Setup

Install Python and JS dependencies:

```bash
uv sync
npm install
```

(Optional) start GROBID:

```bash
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

Override the GROBID URL with `GROBID_URL` if it's not on `localhost:8070`.

(Optional) install olmocr for higher-fidelity PDF → markdown conversion.
It's heavy (vision model, expects a GPU), so it's not in `pyproject.toml`.
Add it to this project's venv if you want it:

```bash
uv add olmocr
```

The backend invokes it via `python -m olmocr.pipeline` by default; override
with `OLMOCR_CMD` (e.g. `OLMOCR_CMD="my-olmocr-wrapper"`) and the per-PDF
timeout with `OLMOCR_TIMEOUT` (seconds, default 900). When olmocr isn't
available the backend silently falls back to `pymupdf4llm`.

## Running

In separate terminals:

```bash
# Backend (FastAPI, http://localhost:8000)
uv run fastapi dev backend/src/CITation/main.py

# Frontend (React, http://localhost:3000)
npm start
```

The frontend talks to the backend at `localhost:8000` by default; override with
the `BACKEND_URL` env var when starting `npm start`. CORS is configured for
`localhost:3000` only.

## API

- `WebSocket /ws/process_pdf` — main pipeline. The client sends paper metadata
  (JSON), file metadata (JSON), then PDF bytes. The server streams `info`
  progress events and a final `end` event with `{citations, authors, venues,
  anomalous, authorGraph}`.
- `POST /api/extract_metadata` — pre-fills the upload form. Accepts a PDF
  multipart upload, reads the first two pages with PyMuPDF, and asks
  `gpt-4o-mini` (JSON mode) for `{title, authors, year}`. The frontend calls
  this as soon as a PDF is dropped so the user reviews/edits rather than
  retypes manuscript metadata; fields stay editable and a warning surfaces if
  extraction fails.
- `POST /api/extract_abstract` — single-PDF abstract extraction via GROBID.
  Requires GROBID.
- `POST /api/extract_abstracts` — batch version.

## Debug outputs

Each pipeline run writes intermediate JSON (enriched papers, citations,
authors, venues, anomalies, author graph, reference mentions, plain text,
formula coordinates, pipeline timing summary) to `outputs/debug/` for
inspection. When the pipeline goes through the markdown fallback (no GROBID,
or GROBID returns no citation mentions), the converted markdown is also
written to `outputs/debug/paper_markdown.md`; on grobid-only runs that file
is removed so the directory doesn't surface stale markdown from a prior run.
The whole `outputs/` directory is gitignored.

The reference-section finder in
[backend/src/CITation/data/process_references.py](backend/src/CITation/data/process_references.py)
prefers an exact heading match (`References`, `Bibliography`, `Works Cited`,
`Literature Cited`) so it doesn't latch onto front-matter sections like
"ACM Reference Format"; it falls back to the *last* heading containing
"reference"/"bibliography" if no exact match is found.

The frontend's WebSocket result handler in [src/App.js](src/App.js) guards
against citations with no resolved author list or venue (the backend leaves
`venue` as `null` when no venue could be inferred) so the page no longer
crashes with `Cannot read properties of null (reading 'includes')` when the
pipeline returns references without venue metadata.

## Tests

```bash
uv run pytest
```

Backend tests live in [backend/tests/](backend/tests/). Mark slow tests with
`@pytest.mark.slow`.

## Legacy scripts

The top-level `*.py` files (`statcheck.py`, `synthetic.py`, `stackinggraph.py`,
`pubmedPaperExtraction.py`, `florMatrix.py`) and [backend_scripts/](backend_scripts/)
are earlier standalone tools that predate the integrated FastAPI pipeline.
They are kept for reference but are not part of the running application.
See [backend_scripts/README.md](backend_scripts/README.md) for the historical
script-by-script pipeline.
