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
- `CREATEAI_SERVICE_TOKEN` set in the environment: a service token for an
  [ASU CreateAI](https://docs.aiml.asu.edu/) project. All LLM calls go through
  CreateAI's OpenAI-compatible API (`CREATEAI_BASE_URL`, default
  `https://api-main.aiml.asu.edu/v1`) using `CREATEAI_MODEL` (default
  `openai/gpt6_1_sol`, GPT‑6.1 Sol). See [LLM model selection](#llm-model-selection).
- `S2_API_KEY` set in the environment ([Semantic Scholar API key](https://www.semanticscholar.org/product/api))
- Docker (optional, to run GROBID locally)

## Quick start

```bash
make dev
```

This installs Python and JS dependencies (re-running only when the lockfiles
change), creates `.env` from [.env.example](.env.example) for your API keys,
starts GROBID in Docker if Docker is available and waits until it's ready
(up to `GROBID_WAIT` seconds, default 180), clears any leftover production
build so `:8000` only serves the API, and runs the backend (`:8000`) and
frontend (`:3000`) together with hot reload. **Open the app at
http://localhost:3000.** Port 8000 is the API only. Opening it in a browser
(e.g. from VS Code's "port is live" prompt) shows a link to `:3000` and
`/docs` instead of a bare 404. VS Code Remote users can add
`"remote.portsAttributes": {"3000": {"onAutoForward": "openBrowser"},
"8000": {"onAutoForward": "silent"}, "8070": {"onAutoForward": "silent"}}`
to `.vscode/settings.json` so the auto-forward prompt opens the UI rather
than the API. Ctrl-C stops both;
`make stop` stops GROBID. `make serve` runs the production build on `:8000`,
and `make help` lists everything else.

API keys can go in `.env` or be exported in your shell.

The sections below describe the manual equivalent.

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
the `REACT_APP_BACKEND_URL` env var when starting `npm start` (e.g.
`REACT_APP_BACKEND_URL=localhost:9000 npm start`). CORS is configured for
`localhost:3000` only.


## LLM model selection

The default model is GPT‑6.1 Sol (`openai/gpt6_1_sol`), chosen for stronger
reference parsing and citation-relevance scoring. The previous default,
`openai/gpt4o`, is no longer offered by CreateAI. Set `CREATEAI_MODEL` to use
another model. To see which IDs your token can use, run:

```bash
curl -s -H "Authorization: Bearer $CREATEAI_SERVICE_TOKEN" \
  https://api-main.aiml.asu.edu/v1/models
```

Models accept different request parameters. GPT‑6.x models, for example,
reject `temperature` and `top_p`. Every LLM call therefore goes through
`llm.chat()` in [llm.py](backend/src/CITation/llm.py), which reads the
model's `supported_parameters` from `/models` once per process and drops any
of `temperature`, `top_p` and `max_tokens` the model doesn't support. For
models that reason by default it also drops `max_tokens`, because reasoning
tokens count against that cap and a small one (such as the 200 used for
relevance scoring) can leave an empty answer. If `/models` can't be fetched,
requests go out unchanged and a warning is logged.


## Deployment

For a web-facing server, build the frontend in production mode and let the
FastAPI app serve it alongside the API:

```bash
npm run build      # writes ./build
uv run fastapi run # serves UI + API on http://0.0.0.0:8000
```

The backend serves the first build it finds among `$FRONTEND_BUILD_DIR`, the
repo-root `build/`, and `backend/src/CITation/build/`. If none exists it runs
API-only, which is what you want in development. The WebSocket uses `wss://`
when the page is loaded over HTTPS and `ws://` otherwise.


## API

- `WebSocket /ws/process_pdf` — main pipeline. The client sends paper metadata
  (JSON), file metadata (JSON), then PDF bytes. The server streams `info`
  progress events and a final `end` event with `{citations, authors, venues,
  anomalous, authorGraph}`.
- `POST /api/extract_metadata` — pre-fills the upload form. Accepts a PDF
  multipart upload, reads the first two pages with PyMuPDF, and asks
  the CreateAI model (JSON mode) for `{title, authors, year}`. The frontend calls
  this as soon as a PDF is dropped so the user reviews/edits rather than
  retypes manuscript metadata; fields stay editable and a warning surfaces if
  extraction fails.
- `POST /api/extract_abstract` — single-PDF abstract extraction via GROBID.
  Requires GROBID.
- `POST /api/extract_abstracts` — batch version.

## Anomaly Anchors

Anomaly payloads now include explicit anchor metadata so the frontend can
resolve each issue to the exact citation marker or statistical expression in
the rendered PDF, instead of relying on page-only navigation.

- Citation anomalies expose `anchors`, where each anchor represents one
  detected in-text marker occurrence with `{page, marker_bbox, page_width,
  page_height, ref_label, sentence}`.
- Citation records returned from `WebSocket /ws/process_pdf` expose
  `cite_positions`, one entry per in-text `[N]` marker. The PDF viewer uses
  these to draw marker-level overlays and associate them with issue IDs.
- When GROBID coordinates are missing, the frontend falls back to the anchor
  sentence and marker label to resolve the highlight in the PDF text layer.
- The anomalies list and detail card now derive their page label from every
  anchor of the issue: a single page renders as `Page: N`, multiple pages as
  `Pages: i, j, k, …`. This also fixes a bug where a paragraph that cited
  several references on different pages could show the wrong page for one of
  them — `assign_scores_to_enriched_papers` previously rebuilt each mention
  dict from a text-only assessment lookup, which dropped `occurrences` and
  let one ref's page overwrite another's. The lookup is now keyed by
  `(ref, excerpt)` and the original mention (including its `occurrences`) is
  preserved.
- Multi-ref groups like `[22,30,32]` are now parsed correctly. GROBID emits
  these as three sibling `<ref>` tags whose visible labels are `"[22,"`,
  `"30,"`, and `"32]"`. The previous `_extract_numeric_label` used
  `re.fullmatch(r"\[?(\d+)\]?", …)`, which failed on the first two (trailing
  comma) and fell back to GROBID's `target="#b…"` attribute — that mapping is
  off-by-one in some papers, so marker "22" was being bucketed under
  `mentions[21]` and surfaced as a stray anchor on page 2. The label parser
  now uses `re.match(r"\[?(\d+)", …)` (leading digit run), so each marker in
  a list binds to the visible number; author-year style labels like
  `"Smith 2020 [5]"` still skip the visible-label path because they don't
  start with `[` or a digit.
- The anomalies list is sorted by **page-then-category**: items are ordered
  by the earliest page they appear on, then within a page by category
  severity (`testFailure` → `selfCitation` → `citationRing` → `unreferenced`
  → `lowRelevancy`). Issues with no page (e.g. unreferenced bibliography
  entries) sink to the bottom; insertion order from the pipeline breaks ties.
- `ref_id` (which becomes `cite_number` shown in the UI) is recovered
  through a three-step fallback when the `<biblStruct>` has no `<label>`
  element: first the leading `[N]` of `<note type="raw_reference">`,
  then a `xml:id → PDF label` map harvested from the fulltext endpoint's
  `<ref type="bibr" target="#bN">[K]</ref>` markers, and only finally
  `enumerate(..., 1)`. GROBID can drop a non-publication entry (e.g. a
  software citation like
  `[1] 2008-2026. GROBID. https://github.com/kermitt2/grobid…`) from the
  bibl list and also omit `<label>` *and* strip the `[N]` prefix from the
  raw reference text — that combination defeats both the label and the
  raw-reference fallbacks, so the fulltext label map is what keeps
  `cite_number` aligned with the source PDF numbering. The pipeline now
  issues the fulltext call before `processReferences` and threads the map
  through `extract_references_with_grobid(..., label_map=…)`.


## Result cache

Results from external services are cached on disk, so re-running a paper
(or a paper that shares references with an earlier one) skips most network
and model work. On `backend/tests/data/sample.pdf` (58 references), the
three GROBID calls plus PDF→markdown take ~126 s cold and ~0.05 s cached.

What is cached, in [cache.py](backend/src/CITation/cache.py) (a single
SQLite file, `.cache/citadel/cache.sqlite3`):

| Namespace  | What                                                | Key                                      | Expires |
|------------|-----------------------------------------------------|------------------------------------------|---------|
| `grobid`   | TEI XML from every GROBID endpoint                  | endpoint + params + PDF content hash     | never   |
| `markdown` | PDF→markdown output, per converter                  | PDF content hash + olmocr/pymupdf4llm    | never   |
| `llm`      | LLM reply text (`llm.chat`)                         | model + messages + params actually sent  | never   |
| `s2`       | Semantic Scholar title search / paper details       | URL + params                             | 30 days |
| `s2_paper` | One paper from S2 `/paper/batch`, cached per paper  | S2 id + requested fields                 | 30 days |
| `openalex` | OpenAlex search, DOI batch, and work lookups        | URL + params                             | 30 days |

Design notes:

- **Only raw responses are cached.** Parsing, enrichment merging, scoring and
  anomaly detection always re-run, so code fixes apply to papers that are
  already cached. A changed prompt, model or request parameter is
  automatically a miss.
- **Failures are never cached.** Only successful responses are stored
  (plus GROBID's 204 "no references" and Semantic Scholar's 404 "no match").
  Empty LLM replies, olmocr failures, 429s, 5xxs and timeouts are retried on
  the next run.
- **S2 batch lookups are cached per paper**, so second-hop references shared
  between manuscripts are fetched only once.
- **Rate limiting only applies to real network calls.** The old fixed 0.5 s
  sleeps after every Semantic Scholar / OpenAlex call are replaced by a
  per-host minimum interval (`request_delay`), so cache hits don't wait.
- API keys are not part of cache keys, and nothing secret is stored.
- `llm.chat()` now returns the reply text instead of the raw completion
  object.
- Each run logs per-namespace hit counts (`Cache: grobid 3/3 hits, …`) and
  records them in `outputs/debug/pipeline_summary.json`.

Controls: `make clear-cache` empties everything, and
`make clear-cache NS=llm` (or any namespace above) clears one source. For
example, clear `grobid` after upgrading GROBID. Set `CITADEL_CACHE=0` to
bypass the cache, `CITADEL_CACHE_DIR` to move it, and
`CITADEL_CACHE_TTL_DAYS` to change how long Semantic Scholar and OpenAlex
entries are kept.


## OpenAlex

OpenAlex is the fallback to Semantic Scholar when enriching cited papers: it
supplies metadata when S2 can't find a paper, ORCIDs when S2's authors lack
them, and the reference list (plus second-hop reference details) when S2 has
none.

- **API key.** Set `OPENALEX_API_KEY` (recommended). Without it, requests count
  against a free daily budget shared by everyone on your IP address; once that
  is used up OpenAlex answers every request with 429 until midnight UTC. The
  key is sent as the `api_key` query parameter and is not part of cache keys
  (`cache.request(..., secret_params=...)`), so adding or changing it doesn't
  invalidate cached responses.
- **429 stops OpenAlex for the run.** The first 429 disables OpenAlex for the
  rest of that pipeline run (`PaperProcessor.openalex_unavailable`) and logs a
  warning, instead of retrying every call three times. The next run tries
  again. Previously an exhausted budget added ~26 s of failing calls and
  sleeps to every run of a 38-reference paper; it now costs one request.
  Affected papers fall back to Semantic Scholar data only, so they may lack
  ORCIDs or second-hop references for that run.
- **Second-hop chunking fix.** OpenAlex reference lists were split with
  `refs[i:i+100] for i in range(0, len(refs), 25)`, so chunks overlapped, and
  each request returned only OpenAlex's default 25 results per page. Second-hop
  references from OpenAlex therefore had duplicates and gaps. Chunks are now
  disjoint (`OPENALEX_CHUNK_SIZE`, 100 ids) and each request sets `per-page` to
  the chunk size. Because the request shape changed, these lookups are fetched
  again once (old cache entries for them are simply unused).
- `retry_api_call` no longer sleeps between attempts; `cache.request` already
  enforces the per-host `request_delay` for real network calls, so the sleep
  only delayed cache hits and fast failures.

## Second-hop references

For every cited paper, the pipeline also fetches that paper's own references
(the "second hop") from Semantic Scholar or OpenAlex and adds them to the
citation graph with `hop: 2`. When neither source has data for one of those
references, `_merge_ref_data` returns an empty record. Previously
`assign_entity_keys_with_refs` then crashed the whole WebSocket run with
`KeyError: 'venue'`. Empty records are now dropped before keys are assigned,
since they would only add blank nodes to the graph. Partial records get
`None` for a missing `venue`, `year` or `doi` instead of raising an error.


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
