import flor
from constants import email, fetch_url

from pymed import PubMed
import requests
import xml.etree.ElementTree as ET
from typing import Set


pubmed = PubMed(tool="PubMedSearcher", email=flor.arg("email", email))
query = f"{flor.arg("kw", "visualization")} AND {flor.arg("year", 2023)}[Date - Publication]"
results = pubmed.query(query, max_results=flor.arg("max_results", 1))

pubmed_ids: Set[int] = set([])
for article in results:
    all_ids = article.pubmed_id.split("\n")
    pubmed_ids |= set([int(pmid) for pmid in all_ids if pmid.isdigit()])

for pmid in flor.loop("pmid", pubmed_ids):
    params = {"db": "pubmed", "id": str(pmid), "retmode": "xml"}
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        metadata = response.text

        # Parse the XML to extract necessary details and reference PMIDs
        root = ET.fromstring(metadata)
        for article in flor.loop("article", root.findall(".//PubmedArticle")):
            flor.log("title", article.findtext(".//ArticleTitle"))
            flor.log("journal", article.findtext(".//Journal/Title"))
            flor.log("authors", [
                author.findtext("LastName") + ", " + author.findtext("ForeName")
                for author in article.findall(".//AuthorList/Author")
                if author.findtext("LastName") and author.findtext("ForeName")
            ])
            flor.log("cited_pmids", [
                ref.text
                for ref in article.findall(
                    ".//Reference/ArticleIdList/ArticleId[@IdType='pubmed']"
                )
            ])
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch metadata for PMID {pmid}: {e}")

    
