# Citadel

Citadel is a web application for reviewing research papers and their citation
networks. Upload a PDF to:

- extract and enrich its references;
- score whether citations are relevant to the surrounding text;
- flag statistical, self-citation, citation-ring, and venue or author
  anomalies;
- build citation, author, and venue graphs; and
- review the findings alongside the original PDF.

## Quick start

### 1. Install the prerequisites

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Node.js 18 or newer and npm
- Docker (optional, but strongly recommended for GROBID)

Without Docker, Citadel can still run, but PDF reference extraction is slower
and less accurate because it falls back to language-model-based conversion.

### 2. Set up the project

From the repository root:

```bash
make setup
```

This installs the Python and JavaScript dependencies and creates `.env` from
[`.env.example`](.env.example).

Open `.env` and add the two required credentials:

```dotenv
CREATEAI_SERVICE_TOKEN=your_createai_token
S2_API_KEY=your_semantic_scholar_key
```

An `OPENALEX_API_KEY` is also recommended. See
[Configuration](#configuration) for details.

### 3. Start the application

```bash
make dev
```

On the first run, the command may take a few minutes while Docker starts
GROBID. Then open:

- **Application:** http://localhost:3000
- **API documentation:** http://localhost:8001/docs

Port `8001` serves only the API during development; use port `3000` for the
user interface.

Stop the backend and frontend with `Ctrl-C`, and stop GROBID with:

```bash
make stop
```

## How to use Citadel

1. Open http://localhost:3000.
2. Upload a research-paper PDF.
3. Review the automatically extracted title, authors, and year.
4. Start the analysis.
5. Inspect anomalies, highlighted PDF locations, and the citation, author, and
   venue graphs.

The first analysis of a paper can take several minutes. Subsequent analyses
benefit from Citadel's local cache.

## Configuration

Credentials and optional settings can be exported in the shell or stored in
`.env`. The Makefile reads `.env` automatically.

| Variable | Requirement | Purpose |
|---|---|---|
| `CREATEAI_SERVICE_TOKEN` | Required | Authenticates LLM calls through ASU CreateAI. |
| `S2_API_KEY` | Required | Authenticates Semantic Scholar metadata requests. |
| `OPENALEX_API_KEY` | Recommended | Avoids the shared OpenAlex free-tier rate limit. |
| `CREATEAI_MODEL` | Optional | Overrides the default `openai/gpt6_1_sol` model. |
| `CREATEAI_BASE_URL` | Optional | Overrides the CreateAI OpenAI-compatible API URL. |
| `GROBID_URL` | Optional | Overrides the default `http://localhost:8070`. |
| `BACKEND_PORT` | Optional | Overrides the API development port, which defaults to `8001`. |
| `REACT_APP_BACKEND_URL` | Optional | Overrides the frontend's development backend address. |
| `OLMOCR_CMD` | Optional | Overrides the optional olmocr command. |
| `OLMOCR_TIMEOUT` | Optional | Sets the olmocr timeout in seconds. |
| `CITADEL_CACHE` | Optional | Set to `0` to disable the result cache. |
| `CITADEL_CACHE_DIR` | Optional | Overrides the default `.cache/citadel` cache directory. |
| `CITADEL_CACHE_TTL_DAYS` | Optional | Sets the Semantic Scholar/OpenAlex cache lifetime. |

`make dev BACKEND_PORT=8002` starts the API on a different port and updates the
frontend's backend URL automatically. Ports `3000`, `8001`, and `8070` must be
available when using the defaults.

### LLM models

Citadel uses the CreateAI OpenAI-compatible API. To list models available to
your token:

```bash
curl -s \
  -H "Authorization: Bearer $CREATEAI_SERVICE_TOKEN" \
  https://api-main.aiml.asu.edu/v1/models
```

Set the selected model ID as `CREATEAI_MODEL` in `.env`. All model requests go
through [`CITation/llm.py`](backend/src/CITation/llm.py), which removes request
parameters unsupported by the selected model.

## Common commands

| Command | Action |
|---|---|
| `make help` | List application targets. |
| `make dev` | Start the API and React development server. |
| `make serve` | Build the frontend and serve the complete app from FastAPI. |
| `make test` | Run the backend test suite. |
| `make grobid` | Start GROBID and wait until it is ready. |
| `make stop` | Stop the GROBID container. |
| `make clear-cache` | Delete all cached external-service results. |
| `make clear-cache NS=llm` | Delete one cache namespace. |

## Manual setup

Use these steps if GNU Make is unavailable.

Install dependencies:

```bash
uv sync
npm install
cp .env.example .env
```

Add the required credentials to `.env`, then start the backend and frontend in
separate terminals:

```bash
# Terminal 1: API on http://localhost:8001
uv run fastapi dev backend/src/CITation/main.py --port 8001

# Terminal 2: application on http://localhost:3000
npm start
```

To run GROBID manually:

```bash
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

The frontend defaults to `localhost:8001`. Override it when starting React if
the API uses another port:

```bash
REACT_APP_BACKEND_URL=localhost:9000 npm start
```

### Optional olmocr support

When GROBID cannot provide the required PDF content, Citadel tries
[olmocr](https://github.com/allenai/olmocr) before falling back to
`pymupdf4llm`. olmocr is optional because it is large and generally expects a
GPU:

```bash
uv add olmocr
```

If olmocr is unavailable, Citadel continues with `pymupdf4llm`.

## Production deployment

Build the frontend and let FastAPI serve both the user interface and API:

```bash
npm run build
uv run fastapi run --port 8001
```

The application is then available at http://localhost:8001. FastAPI searches
for a frontend build in `$FRONTEND_BUILD_DIR`, the repository-level `build/`
directory, and `backend/src/CITation/build/`, in that order.

When the application is loaded over HTTPS, the PDF-processing WebSocket uses
`wss://`; otherwise it uses `ws://`.

## Troubleshooting

### The app opens but analysis fails

- Confirm `CREATEAI_SERVICE_TOKEN` and `S2_API_KEY` are set in `.env`.
- Open `http://localhost:8001/docs` to confirm the API is running.
- If port `8001` is occupied, run `make dev BACKEND_PORT=8002`.
- Check that the frontend is opened at port `3000`, not the API port.

### Reference extraction is slow or low quality

Check that GROBID is available:

```bash
curl http://localhost:8070/api/isalive
```

Start it with `make grobid` or install/start Docker before running
`make dev`.

### OpenAlex requests return 429 errors

Set `OPENALEX_API_KEY` to use a dedicated request budget. Without a key,
OpenAlex uses a small daily allowance shared by the current IP address.
Citadel disables OpenAlex for the remainder of the run after the first `429`
and continues with available Semantic Scholar data.

### Cached data is stale

Clear the cache after changing prompts, external data, or service versions:

```bash
make clear-cache
```

Citadel caches only successful raw responses. Parsing, enrichment, scoring, and
anomaly detection still run for every analysis.

## Architecture

- **Backend:** The FastAPI package is in
  [`backend/src/CITation/`](backend/src/CITation/), with entry point
  `CITation.main:app`.
- **Pipeline:** PDF extraction and enrichment live in
  [`backend/src/CITation/data/`](backend/src/CITation/data/); anomaly
  detection lives in
  [`backend/src/CITation/anomalies/`](backend/src/CITation/anomalies/).
- **Frontend:** The React application is in [`src/`](src/). PDF rendering and
  visualizations are under [`src/components/`](src/components/).
- **GROBID:** Handles reference extraction, citation locations, statistical
  expressions, and missing abstracts when available.
- **Cache:** External responses are stored in a local SQLite database at
  `.cache/citadel/cache.sqlite3`.

## API overview

The backend exposes:

- `WebSocket /ws/process_pdf` — processes an uploaded PDF and streams progress
  plus the final citations, graph data, and anomalies.
- `POST /api/extract_metadata` — extracts the title, authors, and year from
  the first two PDF pages for the upload form.
- `POST /api/extract_abstract` — extracts one PDF abstract through GROBID.
- `POST /api/extract_abstracts` — extracts abstracts from a batch of PDFs.

See http://localhost:8001/docs while the backend is running for interactive
request details.

## Result cache

The cache reduces repeated network and model calls across runs and papers:

| Namespace | Cached data | Lifetime |
|---|---|---|
| `grobid` | GROBID TEI XML | Indefinite |
| `markdown` | PDF-to-markdown output | Indefinite |
| `llm` | LLM reply text | Indefinite |
| `s2` | Semantic Scholar searches and details | 30 days by default |
| `s2_paper` | Individual Semantic Scholar paper records | 30 days by default |
| `openalex` | OpenAlex searches and lookups | 30 days by default |

Failed requests are not cached. Clear the full cache with
`make clear-cache`, or one namespace with, for example,
`make clear-cache NS=grobid`.

## Testing and linting

Run backend tests:

```bash
uv run pytest
```

Build the frontend with warnings treated as errors:

```bash
CI=true npm run build
```

Or run ESLint directly:

```bash
npx eslint --resolve-plugins-relative-to node_modules/react-scripts src
```

## Project layout

```text
backend/src/CITation/  FastAPI backend and integrated processing pipeline
backend/tests/        Backend tests
src/                  React frontend
public/               Frontend static files
known_pdfs/           Example PDFs
backend_scripts/      Legacy standalone pipeline
```

The top-level Python scripts and [`backend_scripts/`](backend_scripts/) are
older standalone experiments that predate the integrated web application.
They are kept for reference and are not required to run Citadel. See the
[legacy pipeline documentation](backend_scripts/README.md) for those scripts.
