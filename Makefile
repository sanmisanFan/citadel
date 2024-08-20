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

# Run the statcheck demo
statcheck: statcheck/statcheckdemo.py
	@echo "Running statcheck"
	cd statcheck && python statcheckdemo.py
	@touch statcheck
	@echo "statcheck done"


# Run the Flask app
run: statcheck
	@echo "Running Flask app"
	@flask run

