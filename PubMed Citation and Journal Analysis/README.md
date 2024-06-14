# PubMed Citation and Journal Analysis

This project aims to analyze citation patterns and journal relationships based on PubMed data. It involves fetching metadata for PubMed articles related to a specified keyword and year, extracting citation information, and building matrices to represent citations between articles and relationships between journals.

## Project Structure

- `main.py`: This script fetches PubMed IDs for articles based on a keyword and year, retrieves metadata for these articles and their references, and saves the combined metadata to a JSON file.
- `matrix.py`: This script loads the metadata JSON file, constructs citation and journal relationship matrices, and identifies pairs of journals with the highest citation counts.

## Setup

### Prerequisites

- Python 3.6 or later
- Required Python packages: `pymed`, `requests`, `xml`, `json`, `numpy`, `pandas`

## Usage

### Fetching Metadata

Run `main.py` to fetch PubMed IDs for articles based on a keyword and year, retrieve metadata for these articles and their references, and save the combined metadata to a JSON file.

Example command:

```bash
python main.py
```

### Analyzing Citation and Journal Relationships

Run matrix.py to load the metadata JSON file, construct citation and journal relationship matrices, and identify pairs of journals with the highest citation counts.

Example command:

```bash
python matrix.py
```
