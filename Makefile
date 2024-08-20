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
parse: $(wildcard known_pdfs/*.pdf)
	@echo "Parsing text"
	python parse.py $(wildcard known_pdfs/*.pdf)
	@touch parse
	@echo "Text parsed"

# Run the statcheck demo
statcheck: statcheck/statcheckdemo.py parse
	@echo "Running statcheck"
	cd statcheck && python statcheckdemo.py
	@touch statcheck
	@echo "statcheck done"


# Run the Flask app
run: statcheck
	@echo "Running Flask app"
	@flask run


# Clean the project
clean:
	@touch statcheck/statcheckdemo.py
	@rm -f parse
