import json
import numpy as np
import pandas as pd

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load data from file
file_path = "papers_metadata.json"
papers = load_json(file_path)

# Extract PMIDs and Journals
pmids = [paper["pmid"] for paper in papers]
journals = list(set(paper["journal"] for paper in papers))

# Initialize Matrices
n_papers = len(pmids)
n_journals = len(journals)

citation_matrix = np.zeros((n_papers, n_papers), dtype=int)
journal_matrix = np.zeros((n_journals, n_journals), dtype=int)

# Create Index Maps
pmid_index = {pmid: index for index, pmid in enumerate(pmids)}
journal_index = {journal: index for index, journal in enumerate(journals)}

# Fill the Matrices
for paper in papers:
    citing_pmid = paper["pmid"]
    citing_index = pmid_index[citing_pmid]
    citing_journal_index = journal_index[paper["journal"]]
    for cited_pmid in paper["cited_pmids"]:
        if cited_pmid in pmid_index:
            cited_index = pmid_index[cited_pmid]
            cited_journal_index = journal_index[next(p["journal"] for p in papers if p["pmid"] == cited_pmid)]
            citation_matrix[citing_index, cited_index] = 1
            journal_matrix[citing_journal_index, cited_journal_index] += 1

# Convert to DataFrame for better visualization
citation_df = pd.DataFrame(citation_matrix, index=pmids, columns=pmids)
journal_df = pd.DataFrame(journal_matrix, index=journals, columns=journals)

# Save to CSV
citation_df.to_csv("citation_matrix.csv")
journal_df.to_csv("journal_matrix.csv")

# Find the pairs of papers with the highest citation counts



# Find the pairs of journals with the highest citation counts
max_journal_citations = np.max(journal_matrix)
max_journal_citation_pairs = np.argwhere(journal_matrix == max_journal_citations)

# Display the results for journals
print(f"\nPairs of journals with the highest citation count ({max_journal_citations}):")
for pair in max_journal_citation_pairs:
    citing_journal = journals[pair[0]]
    cited_journal = journals[pair[1]]
    print(f"Citing Journal: {citing_journal}, Cited Journal: {cited_journal}, Count: {journal_matrix[pair[0], pair[1]]}")
