import json
import numpy as np
import pandas as pd
import flor

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

# Log summary statistics for citations
total_citations = np.sum(citation_matrix)
unique_citing_papers = np.count_nonzero(np.sum(citation_matrix, axis=1))

flor.log("total_citations", {"total": total_citations, "unique_citing_papers": unique_citing_papers})

# Find the pairs of journals with the highest citation counts
max_journal_citations = np.max(journal_matrix)
max_journal_citation_pairs = np.argwhere(journal_matrix == max_journal_citations)

# Log max citation journal pairs
max_journal_pairs = []
for pair in max_journal_citation_pairs:
    citing_journal = journals[pair[0]]
    cited_journal = journals[pair[1]]
    max_journal_pairs.append({
        "citing_journal": citing_journal,
        "cited_journal": cited_journal,
        "count": journal_matrix[pair[0], pair[1]]
    })

flor.log("max_journal_citations", {
    "max_citation_count": max_journal_citations,
    "max_journal_pairs": max_journal_pairs
})

### Additional Code for the Author Matrix ###

# Step 1: Extract unique authors
unique_authors = set()
for paper in papers:
    unique_authors.update(paper["authors"])

# Step 2: Convert the set of unique authors to a list
unique_authors = list(unique_authors)

# Step 3: Initialize the author matrix
n_authors = len(unique_authors)
author_matrix = np.zeros((n_authors, n_authors), dtype=int)

# Step 4: Create an index map for authors
author_index = {author: index for index, author in enumerate(unique_authors)}

# Step 5: Fill the matrix based on co-authorship
for paper in papers:
    authors = paper["authors"]
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):  # Avoid self-loops and redundant pairs
            author1_index = author_index[authors[i]]
            author2_index = author_index[authors[j]]
            author_matrix[author1_index, author2_index] += 1
            author_matrix[author2_index, author1_index] += 1  # Matrix is symmetric

# Convert author matrix to DataFrame
author_df = pd.DataFrame(author_matrix, index=unique_authors, columns=unique_authors)

# Log summary statistics for co-authorship
total_coauthorships = np.sum(author_matrix) // 2  # Since matrix is symmetric, divide by 2
max_coauthorship_count = np.max(author_matrix)

flor.log("coauthorship_summary", {
    "total_coauthorships": total_coauthorships,
    "max_coauthorship_count": max_coauthorship_count
})

# Display some information about the author matrix
print(f"\nTotal Co-authorships: {total_coauthorships}")
print(f"Max Co-authorship Count between any two authors: {max_coauthorship_count}")


most_cited_paper_index = np.argmax(cited_distribution)
most_cited_paper = pmids[most_cited_paper_index]
most_cited_paper_count = cited_distribution[most_cited_paper_index]

flor.log("most_cited_paper", {
    "pmid": most_cited_paper,
    "citation_count": most_cited_paper_count
})