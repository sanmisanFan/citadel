import requests
import pandas as pd
import xml.etree.ElementTree as ET

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_metadata(pmids):
    fetch_url = f"{base_url}efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    response = requests.get(fetch_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata for PMIDs: {response.status_code}")
    return response.text

pmids = ['38867889', '38855758']

# Fetch metadata for the given PMIDs
metadata_xml = fetch_metadata(pmids)

# Print the fetched metadata (in XML format)
print(metadata_xml)