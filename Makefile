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


# Run the Flask app
run: statcheck
	@echo "Running Flask app"
	@flask run


# Clean the project
clean:
	@rm -f statcheck
	@rm -f parse
	@rm -f ~/.flor/research_reviewer_main.db
