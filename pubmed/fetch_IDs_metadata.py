import flor
from constants import email

from pymed import PubMed


pubmed = PubMed(tool="PubMedSearcher", email=flor.arg("email", email))
query = f"{flor.arg("kw", "visualization")} AND {flor.arg("year", 2023)}[Date - Publication]"
results = pubmed.query(query, max_results=flor.arg("max_results", 1))

for article in flor.loop("article", results):
    pubmed_ids = article.pubmed_id.split("\n")
    pubmed_ids = [int(pmid) if pmid.isdigit() else None for pmid in pubmed_ids]
    for pmid in flor.loop("pmid", pubmed_ids):
        pass

    
