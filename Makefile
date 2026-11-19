# =============================================================================
# Citadel app
#
#   make dev     install deps if needed, start GROBID, run backend + frontend
#   make serve   production build served by FastAPI on :$(BACKEND_PORT) (18081)
#   make help    list all targets
#
# API keys are read from the environment or from a .env file (KEY=value lines,
# no quotes). `make setup` creates .env from .env.example on first run.
# =============================================================================

-include $(wildcard .env)
export

GROBID_URL       ?= http://localhost:8070
GROBID_IMAGE     ?= lfoppiano/grobid:0.8.0
GROBID_CONTAINER ?= citadel-grobid
GROBID_WAIT      ?= 180
BACKEND_PORT     ?= 18081
# Where the dev frontend sends API calls (exported to `npm start`).
REACT_APP_BACKEND_URL ?= localhost:$(BACKEND_PORT)

.DEFAULT_GOAL := help

.PHONY: help setup dev run backend frontend build clean-build serve test grobid grobid-stop stop check-env clear-cache

run: dev

help:
	@echo "Citadel targets:"
	@echo "  make setup        install Python + JS deps, create .env"
	@echo "  make dev          backend (:$(BACKEND_PORT)) + frontend (:3000) with hot reload"
	@echo "  make serve        build frontend, serve everything from FastAPI (:$(BACKEND_PORT))"
	@echo "  make test         run backend tests"
	@echo "  make grobid       start GROBID and wait until ready (also done by dev/serve)"
	@echo "  make stop         stop the GROBID container"
	@echo "  make clear-cache  empty the result cache (NS=grobid|s2|s2_paper|openalex|llm|markdown for one source)"

setup: .venv/.uv-synced node_modules/.npm-installed .env

# Re-sync only when the lockfiles change.
.venv/.uv-synced: pyproject.toml uv.lock
	@command -v uv >/dev/null || { echo "uv not found: install it from https://docs.astral.sh/uv/"; exit 1; }
	uv sync
	@touch $@

node_modules/.npm-installed: package.json package-lock.json
	@command -v npm >/dev/null || { echo "npm not found: install Node.js from https://nodejs.org/"; exit 1; }
	npm install
	@touch $@

.env:
	@cp .env.example .env
	@echo "Created .env: fill in CREATEAI_SERVICE_TOKEN and S2_API_KEY, then re-run make."

check-env:
	@test -n "$$CREATEAI_SERVICE_TOKEN" || { echo "CREATEAI_SERVICE_TOKEN is not set (add it to .env)"; exit 1; }
	@test -n "$$S2_API_KEY" || { echo "S2_API_KEY is not set (add it to .env)"; exit 1; }

# GROBID is optional: skip with a warning if Docker isn't available. Otherwise
# start the container if needed and block until it answers /api/isalive.
grobid:
	@python3 scripts/run_dev.py

# Remove production builds so the dev backend doesn't serve a stale UI on :$(BACKEND_PORT).
clean-build:
	rm -rf build backend/src/CITation/build

# Empty the external-service result cache (see backend/src/CITation/cache.py).
# NS=<namespace> clears one source only, e.g. `make clear-cache NS=llm`.
clear-cache: .venv/.uv-synced
	@uv run python -c "import sys; from CITation import cache; ns = sys.argv[1] or None; print(f'Deleted {cache.clear(ns)} cached entries', f'from {ns}' if ns else '')" "$(NS)"

grobid-stop stop:
	@docker stop $(GROBID_CONTAINER) >/dev/null 2>&1 && echo "Stopped GROBID" || echo "GROBID container not running"

dev: setup check-env
	@.venv/bin/python scripts/run_dev.py "$(MAKE_COMMAND)"

backend: .venv/.uv-synced clean-build
	uv run fastapi dev backend/src/CITation/main.py --port $(BACKEND_PORT)

frontend: node_modules/.npm-installed
	npm start

build: node_modules/.npm-installed
	npm run build

serve: setup check-env grobid build
	uv run fastapi run --port $(BACKEND_PORT)

test: .venv/.uv-synced
	uv run pytest

# =============================================================================
# Legacy standalone scripts (predate the FastAPI pipeline; see README)
# =============================================================================

.PHONY: all clean extractor process_references raw_ref_to_json summarize gpt_relevance cit_locator second_hop citation_graph_builder paper_details generate_anomalous_json author_sus venue_sus visualize_citation_network

#  _____ __    _____ _____ _____ __    _____ _____
# |   __|  |  |     | __  |  _  |  |  |  _  |   | |
# |   __|  |__|  |  |    -|   __|  |__|     | | | |
# |__|  |_____|_____|__|__|__|  |_____|__|__|_|___|
#

# backend_all: extractor process_references raw_ref_to_json summarize gpt_relevance cit_locator second_hop citation_graph_builder paper_details generate_anomalous_json author_sus venue_sus

# Targets for Python scripts
extractor:
	@echo "Running extractor.py..."
	cd backend_scripts && python extractor.py

process_references:
	@echo "Running process_references.py..."
	python backend_scripts/process_references.py

raw_ref_to_json:
	@echo "Running raw_ref_to_json.py..."
	python backend_scripts/raw_ref_to_json.py

summarize:
	@echo "Running summarize.py..."
	python backend_scripts/summarize.py

gpt_relevance:
	@echo "Running gpt_relevance.py..."
	python backend_scripts/gpt_relevance.py

cit_locator:
	@echo "Running cit_locator.py..."
	python backend_scripts/cit_locator.py

second_hop:
	@echo "Running second_hop.py..."
	python backend_scripts/second_hop.py

citation_graph_builder:
	@echo "Running citation_graph_builder.py..."
	python backend_scripts/citation_graph_builder.py

paper_details:
	@echo "Running paper_details.py..."
	python backend_scripts/paper_details.py

generate_anomalous_json:
	@echo "Running generate_anomalous_json.py..."
	python backend_scripts/generate_anomalous_json.py

# Targets for subdirectories (if applicable)
author_sus:
	@echo "Running author.sus..."
	python backend_scripts/author_sus.py

venue_sus:
	@echo "Running venue.sus..."
	python backend_scripts/venue_sus.py


# Parse text
parse: $(wildcard known_pdfs/*.pdf) parse_text.py
	@echo "Parsing text"
	python parse_text.py $(wildcard known_pdfs/*.pdf)
	@touch parse
	@echo "Text parsed"

# Run the statcheck demo
statcheck: parse statcheck.py
	@echo "Running statcheck"
	python statcheck.py
	@touch statcheck
	@echo "statcheck done"

# Generate citation network
generate_citation_network: synthetic.py
	@echo "Generating citation network"
	python synthetic.py --kwargs num_papers=10
	@touch generate_citation_network
	@echo "Citation network generated"


visualize_citation_network: generate_citation_network stackinggraph.py
	@echo "Visualizing citation network"
	python stackinggraph.py
	@echo "Citation network visualized"

fetch_pubmed: pubmed/fetch_IDs_metadata.py
	@echo "Fetching PubMed metadata"
	python pubmed/fetch_IDs_metadata.py
	@touch fetch_pubmed
	@echo "PubMed data fetched"



# Clean the project
clean:
	@rm -f statcheck
	@rm -f parse
	@rm -f generate_citation_network
	@rm -f fetch_pubmed
	@rm -f ~/.flor/research_reviewer_main.db
	@rm -rf outputs/*


.PHONY: 