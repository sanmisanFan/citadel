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

When the markdown fallback path runs through olmocr, the converter in
[backend/src/CITation/data/olmocr.py](backend/src/CITation/data/olmocr.py)
emits `<!-- olmocr-page: N -->` HTML-comment markers at page boundaries
(derived from olmocr's Dolma `attributes.pdf_page_numbers` spans), and
`group_references_by_number` tracks the current page to attach a real
`page` number to each citation mention — matching the schema GROBID
produces. Without these markers the markdown-fallback path defaulted every
mention to page 1, which surfaced in the UI as "Page: 1" on every anomaly.

The frontend's WebSocket result handler in [src/App.js](src/App.js) guards
against citations with no resolved author list or venue (the backend leaves
`venue` as `null` when no venue could be inferred) so the page no longer
crashes with `Cannot read properties of null (reading 'includes')` when the
pipeline returns references without venue metadata.

`generate_scc_anomalies` in
[backend/src/CITation/anomalies/detect_anomalies.py](backend/src/CITation/anomalies/detect_anomalies.py)
now reads the page number from the first `reference_mentions` entry instead
of hardcoding `page: 1`, so self-citation / citation-ring anomalies surface
on the page where the citation actually appears (matching what the
low-relevancy code path already did).

`parse_citation_mentions` in
[backend/src/CITation/data/grobid.py](backend/src/CITation/data/grobid.py)
now reads the page number from each `<ref>` element's own `coords`
attribute (the actual citation-marker location) and only falls back to the
enclosing paragraph's `coords` when the `<ref>` has none. The previous
implementation always used the paragraph coords, which reported the page
the paragraph *starts on* — wrong whenever a paragraph spans pages — and
left the page at the default `1` whenever the paragraph element had no
coords. This is what was causing every anomaly to appear with "Page: 1"
in the UI and the click-to-scroll handler in
[src/components/pdfContainer/index.js](src/components/pdfContainer/index.js)
to always jump to page 1.

Self-citation is now only flagged when a cited author is also an author of
the manuscript being reviewed. The previous SCC self-edge fallback in
`generate_scc_anomalies` / `update_anomalous_with_hop1_sccs`
([backend/src/CITation/anomalies/detect_anomalies.py](backend/src/CITation/anomalies/detect_anomalies.py))
labeled hop-1 papers as "Self Citation" whenever any of their authors had a
self-loop in the SCC graph (i.e. the author cited themselves over time),
which produced false positives on references whose authors were unrelated to
the manuscript. Those references now fall through to "Citation Ring" when
they meet the SCC criterion.

`build_suspicious_authors_graph` in
[backend/src/CITation/anomalies/author_sus.py](backend/src/CITation/anomalies/author_sus.py)
now requires suspicious SCCs to contain **at least two authors**
(`2 <= len(scc) <= 8` instead of `1 <= ...`). A size-1 SCC is a single
author with a self-loop — i.e. heavy self-citation across their own papers —
which is normal behavior for prolific authors (e.g. Daniel Kahneman citing
his own work) and is not a "ring" by any sensible definition. The previous
threshold flagged those authors as being in a citation-ring group, which
then propagated to every hop-1 paper they wrote, producing false-positive
"Citation Ring" anomalies on celebrity references.

A new `Unreferenced` citation anomaly flags bibliography entries that never
appear in the body of the manuscript. `generate_unreferenced_anomalies` in
[backend/src/CITation/anomalies/detect_anomalies.py](backend/src/CITation/anomalies/detect_anomalies.py)
walks the enriched papers and emits an issue for any reference with no
`reference_mentions`. The frontend has a corresponding color in
[src/annotationConfig.js](src/annotationConfig.js) and renders an
"Unreferenced" tag plus tooltip in
[src/components/visContainer/anomalousList.js](src/components/visContainer/anomalousList.js),
[src/components/visContainer/contentCard.js](src/components/visContainer/contentCard.js),
and
[src/components/visContainer/authorInfoCard.js](src/components/visContainer/authorInfoCard.js).
Because unreferenced entries have no body location, the issue is emitted
with `page: null` and an empty sentence; the anomaly list renders a "—" in
the page column and [src/App.js](src/App.js) skips registering a body
highlight for these issues.

UI labels were tightened to use the noun "Anomaly"/"Anomalies" instead of
the adjective "Anomalous": citation issues now display as "Citation Anomaly"
(emitted by `detect_anomalies.py`), the details card uses an "Anomaly" row,
and the overview / floating legend read "Anomaly Overview" and "Detected
Anomalies Legend".

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
