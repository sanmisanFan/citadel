.PHONY: all clean extractor process_references raw_ref_to_json summarize gpt_relevance cit_locator second_hop citation_graph_builder paper_details generate_anomalous_json author_sus venue_sus

#  _____ __    _____ _____ _____ __    _____ _____ 
# |   __|  |  |     | __  |  _  |  |  |  _  |   | |
# |   __|  |__|  |  |    -|   __|  |__|     | | | |
# |__|  |_____|_____|__|__|__|  |_____|__|__|_|___|
#                                 

# Install the required packages
install:
	@echo "Installing required packages"
	@pip install -r requirements.txt
	@echo "Packages installed"


# Targets for Python scripts
extractor:
	@echo "Running extractor.py..."
	python backend_scripts/extractor.py

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

# Run the Flask app
run: statcheck
	@echo "Running Flask app"
	@flask run


# Create a virtual environment
create_venv:
		@if [ ! -d ".venv" ]; then \
				echo "Creating virtual environment..."; \
				python3 -m venv .venv; \
		fi

# Clean the project
clean:
	@rm -f statcheck
	@rm -f parse
	@rm -f generate_citation_network
	@rm -f fetch_pubmed
	@rm -f ~/.flor/research_reviewer_main.db
	@rm -rf outputs/*


.PHONY: install run clean visualize_citation_network create_venv