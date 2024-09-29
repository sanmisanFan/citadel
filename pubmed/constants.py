import os

# Base URL for NCBI Entrez utilities
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Get the right user email for the PubMed API
user_name = os.getenv("USER")
if "akshit" in user_name:
    email = "akshitjain434303@gmail.com"
elif "garci" in user_name:
    email = "rolando.garcia@asu.edu"
else:
    email = input("Enter your email for the PubMed API: ").strip()

__all__ = ["base_url", "email"]
