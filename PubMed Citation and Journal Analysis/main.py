import requests
import xml.etree.ElementTree as ET
import json
from pymed import PubMed

# Function to fetch PubMed IDs based on a keyword and year
def fetch_pubmed_ids(keyword, year):
    pubmed = PubMed(tool="PubMedSearcher", email="akshitjain434303@gmail.com")
    query = f"{keyword} AND {year}[Date - Publication]"
    results = pubmed.query(query, max_results=4)
    
    pubmed_ids = []
    for article in results:
        pubmed_ids.append(article.pubmed_id.split('\n')[0])
    
    return pubmed_ids

# Base URL for NCBI Entrez utilities
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Function to fetch metadata for a list of PubMed IDs
def fetch_metadata(pmids, batch_size=10):
    fetch_url = f"{base_url}efetch.fcgi"
    all_metadata = []
    all_references = set()  # Use a set to avoid duplicates
    extracted_data = []

    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i:i+batch_size]
        params = {
            "db": "pubmed",
            "id": ",".join(batch_pmids),
            "retmode": "xml"
        }
        try:
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            all_metadata.append(response.text)

            # Parse the XML to extract necessary details and reference PMIDs
            root = ET.fromstring(response.text)
            for article in root.findall(".//PubmedArticle"):
                title = article.findtext(".//ArticleTitle")
                journal = article.findtext(".//Journal/Title")
                authors = [author.findtext("LastName") + ", " + author.findtext("ForeName")
                           for author in article.findall(".//AuthorList/Author")
                           if author.findtext("LastName") and author.findtext("ForeName")]

                cited_pmids = [ref.text for ref in article.findall(".//Reference/ArticleIdList/ArticleId[@IdType='pubmed']")]
                for ref in cited_pmids:
                    all_references.add(ref)

                extracted_data.append({
                    "pmid": article.findtext(".//PMID"),
                    "title": title,
                    "journal": journal,
                    "authors": authors,
                    "cited_pmids": cited_pmids
                })
                    
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch metadata for PMIDs {batch_pmids}: {e}")
    
    return extracted_data, list(all_references)

# Define the keyword and year for the PubMed search
keyword = "machine learning"
year = "2023"

# Fetch PubMed IDs based on the given keyword and year
pmids = fetch_pubmed_ids(keyword, year)
print("Fetched PubMed IDs:", pmids)

# Fetch initial metadata and extract references
initial_metadata, reference_pmids = fetch_metadata(pmids)
print("Initial Metadata:", initial_metadata)
print("Reference PMIDs:", reference_pmids)

# Fetch metadata for the reference PMIDs
reference_metadata, _ = fetch_metadata(reference_pmids)
print("Reference Metadata:", reference_metadata)

# Combine initial and reference metadata
combined_metadata = initial_metadata + reference_metadata

# Save the combined metadata to a JSON file
with open("papers_metadata.json", "w") as json_file:
    json.dump(combined_metadata, json_file, indent=4)
