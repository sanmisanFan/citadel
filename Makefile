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
	@rm -f ~/.flor/research_reviewer_main.db


.PHONY: install run clean visualize_citation_network create_venv