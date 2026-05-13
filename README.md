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

The anomaly click-to-scroll handler in
[src/components/pdfContainer/index.js](src/components/pdfContainer/index.js)
now verifies the rendered PDF text for the actual inline citation marker
(for example `[7]`) before falling back to the backend-provided anomaly
page. This prevents jumps to stale pages when the pipeline returns a
citation-ring/self-citation anomaly with an empty sentence and a misaligned
page number, which is currently possible when upstream citation-mention
mapping is off.

GROBID reference-mention parsing in
[backend/src/CITation/data/grobid.py](backend/src/CITation/data/grobid.py)
now prefers the visible TEI citation label (`[22]`, `[7]`, etc.) for both
bibliography `ref_id` assignment and in-text mention mapping, only falling
back to internal `target="#bN"` ids when no numeric label text is present.
This avoids the upstream mismatch where GROBID's internal bibliography ids
drift from the manuscript's displayed numbering and page-3 mention text gets
attached to the wrong citation number.

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

Clicking an anomaly card now reliably highlights the relevant sentence on
the target page. The PDF viewer in
[src/components/pdfContainer/index.js](src/components/pdfContainer/index.js)
previously gated `applyHighlightsReact` on `onRenderSuccess`, which fires
when each page's *canvas* finishes — but the text layer (whose spans
`findSentenceInTextLayer` walks) is built afterwards, so highlights raced
the text layer and intermittently failed with `[Highlight] Sentence not
found`. The viewer now tracks `onRenderTextLayerSuccess` instead, and the
callback is wrapped in `useCallback` with no per-page closure so its
identity is stable across renders. react-pdf's TextLayer lists
`onRenderSuccess` in its layout-effect dependencies
(`node_modules/react-pdf/dist/cjs/Page/TextLayer.js`), so a fresh arrow
function instance on every parent re-render — caused by the scroll
handler's `setCurrentPage` call and clicks updating `activeHighlight` —
cancelled the in-flight text-layer render and restarted it, producing
thousands of `TextLayer task cancelled` console warnings and preventing
`onRenderTextLayerSuccess` from ever firing for the destination page. With
a stable callback the text layer renders once and the highlight applies
on first click. `findSentenceInTextLayer` in
[src/util/pdfUtil.js](src/util/pdfUtil.js) also normalises common unicode
variants that diverge between PDF.js text-layer output and the
GROBID-extracted backend sentence (ligatures `ﬁ`/`ﬂ`, smart quotes, em/en
dashes, soft hyphens, non-breaking spaces) via NFKC, and stitches words
broken across spans by line-break hyphenation (e.g. `"anom-"` + `"aly"` →
`"anomaly"`) so the broken word matches the backend's unhyphenated form.
On top of that, a last-resort alphanumeric-only pass (`normAlnum`) runs
when basic and aggressive matching both fail, with a leading-prefix
fallback that walks back from the full target length so a tail mismatch
doesn't lose the whole match. This tolerates punctuation/whitespace
discrepancies inside citation lists (`[22,30,32]` vs `[22, 30, 32]`) and
the multi-sentence excerpts GROBID sometimes returns when its sentence
splitter misses a boundary in the extracted mention text.

When the citation marker is nowhere in the GROBID paragraph handed to
`extract_citation_sentence` ([backend/src/CITation/anomalies/detect_anomalies.py](backend/src/CITation/anomalies/detect_anomalies.py)),
the function now returns `""` instead of the paragraph's first 200
characters. The old fallback silently attributed every such anomaly to
the same paragraph-opening string, so distinct citations collapsed onto
one (often un-locatable) sentence and the frontend logged repeated
`[Highlight] Sentence not found` warnings. Empty sentences are already
treated as "no body location" by [src/App.js](src/App.js) — the anomaly
is still listed but no sentence underline is drawn.

To make the active anomaly unambiguous when several share a line, the
sentence underline in
[src/components/issueComps/sentenceAnnotate.js](src/components/issueComps/sentenceAnnotate.js)
is now muted (`opacity: 0.35`, 2px) for inactive issues and bold (full
opacity, 3px) for the selected one — previously only the background
differed, so a selected anomaly whose sentence couldn't be located
looked indistinguishable from neighbouring anomalies' underlines.
[src/components/issueComps/highlightBox.js](src/components/issueComps/highlightBox.js)
also now activates a citation-marker bbox when *any* issue in
`cite.issues` matches `activeHighlight` (previously only
`cite.issues[0]` was checked, so secondary issues never lit up their
marker). Finally, the selection effect in
[src/components/pdfContainer/index.js](src/components/pdfContainer/index.js)
now scrolls to the citation-marker bbox when one is available, instead
of just to the top of the page — so clicking an anomaly whose sentence
can't be matched still anchors the viewport on the `[N]` marker.

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
