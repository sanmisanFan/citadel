import os
import requests
import xml.etree.ElementTree as ET
import flor
import pandas as pd
from pymed import PubMed

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


# Function to fetch PubMed IDs based on a keyword and year
def fetch_pubmed_ids(keyword, year):
    pubmed = PubMed(tool="PubMedSearcher", email=flor.arg("email", email))
    query = f"{keyword} AND {year}[Date - Publication]"
    results = pubmed.query(query, max_results=1)

    pubmed_ids = []
    for article in results:
        pubmed_ids.append(article.pubmed_id.split("\n")[0])

    return pubmed_ids


# Function to fetch metadata for a list of PubMed IDs
def fetch_metadata(pmids, batch_size=1):
    fetch_url = f"{base_url}efetch.fcgi"
    all_metadata = []
    all_references = set()  # Use a set to avoid duplicates
    extracted_data = []

    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i : i + batch_size]
        params = {"db": "pubmed", "id": ",".join(batch_pmids), "retmode": "xml"}
        try:
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            all_metadata.append(response.text)

            # Parse the XML to extract necessary details and reference PMIDs
            root = ET.fromstring(response.text)
            for article in root.findall(".//PubmedArticle"):
                title = article.findtext(".//ArticleTitle")
                journal = article.findtext(".//Journal/Title")
                authors = [
                    author.findtext("LastName") + ", " + author.findtext("ForeName")
                    for author in article.findall(".//AuthorList/Author")
                    if author.findtext("LastName") and author.findtext("ForeName")
                ]

                cited_pmids = [
                    ref.text
                    for ref in article.findall(
                        ".//Reference/ArticleIdList/ArticleId[@IdType='pubmed']"
                    )
                ]
                for ref in cited_pmids:
                    all_references.add(ref)

                extracted_data.append(
                    {
                        "pmid": article.findtext(".//PMID"),
                        "title": title,
                        "journal": journal,
                        "authors": authors,
                        "cited_pmids": cited_pmids,
                    }
                )

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch metadata for PMIDs {batch_pmids}: {e}")

    return extracted_data, list(all_references)


# Define the keyword and year for the PubMed search
keyword = "visualization"
year = "2023"

# Fetch PubMed IDs based on the given keyword and year
pmids = fetch_pubmed_ids(keyword, year)
print("Fetched PubMed IDs:", pmids)

"""
DONE
"""

# Fetch initial metadata and extract references
initial_metadata, reference_pmids = fetch_metadata(pmids)
print("Initial Metadata:", initial_metadata)
print("Reference PMIDs:", reference_pmids)

# Fetch metadata for the reference PMIDs
reference_metadata, _ = fetch_metadata(reference_pmids)
print("Reference Metadata:", reference_metadata)

# Combine initial and reference metadata
combined_metadata = initial_metadata + reference_metadata


### Using FlorDB ###

# Convert JSON data into a DataFrame
combined_metadata_df = pd.DataFrame(combined_metadata)

# Convert 'authors' and 'cited_pmids' lists to comma-separated strings
combined_metadata_df["authors"] = combined_metadata_df["authors"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else ""
)
combined_metadata_df["cited_pmids"] = combined_metadata_df["cited_pmids"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else ""
)

# Ensure column names are unique
if not combined_metadata_df.columns.is_unique:
    print("Found duplicated columns, removing duplicates...")
    combined_metadata_df = combined_metadata_df.loc[
        :, ~combined_metadata_df.columns.duplicated()
    ]

# Convert the entire DataFrame to strings to ensure compatibility
combined_metadata_df = combined_metadata_df.astype(str)

# Print column names to confirm
print("Column names:", combined_metadata_df.columns)

# Loop through each row in the DataFrame and log data to FlorDB
for index, row in flor.loop("paper", combined_metadata_df.iterrows()):
    row_dict = row.to_dict()  # Convert row into a dictionary
    flor.log(
        f"row", row_dict
    )  # Log the dictionary to FlorDB with a unique name for each row
    print(f"Stored row {index} in FlorDB.")

print("Combined metadata has been stored in FlorDB.")
