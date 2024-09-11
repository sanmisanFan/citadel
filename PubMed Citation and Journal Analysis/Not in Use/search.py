from pymed import PubMed

def fetch_pubmed_ids(keyword, year):
    pubmed = PubMed(tool="PubMedSearcher", email="akshitjain434303@gmail.com")
    query = f"{keyword} AND {year}[Date - Publication]"
    results = pubmed.query(query, max_results=2)
    
    pubmed_ids = []
    for article in results:
        pubmed_ids.append(article.pubmed_id.split('\n')[0])
    
    return pubmed_ids

if __name__ == "__main__":
    keyword = "machine learning"
    year = "2023"

    pubmed_ids = fetch_pubmed_ids(keyword, year)
    print(pubmed_ids)