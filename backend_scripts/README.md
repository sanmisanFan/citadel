# Citation Processing Pipeline

This project processes a PDF research paper to extract references, enrich them with metadata, summarize cited papers, assess citation relevance, locate citations in the PDF, fetch second-hop references, and generate structured JSON outputs (citations, authors, venues).

---

## ✨ Prerequisites

- Python 3.x
- Install dependencies:

  ```bash
  pip install requests openai PyPDF2 PyMuPDF nltk marker-pdf
  ```

- **OpenAI API Key**: Set your API key as an environment variable:

  - Unix:
    ```bash
    export OPENAI_API_KEY=your_key
    ```
  - Windows:
    ```bash
    set OPENAI_API_KEY=your_key
    ```

- **Input Files**:

  - Place `test.pdf` (your main research paper) in the root directory.
  - Place PDFs of referenced papers in the `reference_papers/` folder.

- **Directory**:
  - Create an `outputs/` folder for results.

---

## ⚙️ Scripts and Execution Order

Run the scripts **in the following order** to ensure proper data flow:

### 1. `extractor.py`

- Converts `test.pdf` to Markdown and JSON using the `marker` CLI tool.
- **Input**: `test.pdf`
- **Output**:
  - `outputs/test/test.md`
  - `outputs/test/test.json`
- **Run**:
  ```bash
  python extractor.py
  ```
- Note: Install `marker` via `pip install marker`.

### 2. `process_references.py`

- Extracts citation mentions and the references section.
- **Input**: `outputs/test/test.md`
- **Output**:
  - `outputs/reference_mentions.json`
  - `outputs/rawreferences.txt`
- **Run**:
  ```bash
  python process_references.py
  ```

### 3. `raw_ref_to_json.py`

- Parses raw references with GPT and enriches them with metadata.
- **Input**:
  - `outputs/rawreferences.txt`
  - `outputs/reference_mentions.json`
- **Output**:
  - `outputs/enriched_papers.json`
  - `outputs/entity_keys.json`
- **Run**:
  ```bash
  python raw_ref_to_json.py
  ```

### 4. `summarize.py`

- Summarizes referenced papers using GPT.
- **Input**: `reference_papers/*.pdf`
- **Output**: `outputs/pdf_summaries.json`
- **Run**:
  ```bash
  python summarize.py
  ```

### 5. `gpt_relevance.py`

- Uses GPT to score citation relevance.
- **Input**:
  - `outputs/reference_mentions.json`
  - `outputs/pdf_summaries.json`
  - `outputs/enriched_papers.json`
- **Output**:
  - `outputs/detailed_citation_assessments.json`
  - `outputs/enriched_papers_with_scores.json`
- **Run**:
  ```bash
  python gpt_relevance.py
  ```

### 6. `cit_locator.py`

- Locates and annotates citation mentions in the original PDF.
- **Input**:
  - `test.pdf`
  - `outputs/enriched_papers_with_scores.json`
- **Output**:
  - `outputs/annotated_test.pdf`
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/annotated_results.json`
- **Run**:
  ```bash
  python cit_locator.py
  ```

### 7. `second_hop.py`

- Fetches second-hop citations and updates the graph.
- **Input**:
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/second_hop_references.json`
  - Updates `outputs/entity_keys.json`
- **Run**:
  ```bash
  python second_hop.py
  ```

### 8. `citation_graph_builder.py`

- Builds final citation, author, and venue graphs.
- **Input**:
  - `outputs/enriched_papers_with_bboxes.json`
  - `outputs/second_hop_references.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/citations.json`
  - `outputs/authors.json`
  - `outputs/venues.json`
- **Run**:
  ```bash
  python citation_graph_builder.py
  ```

### 9. `paper_details.py`

- Adds the primary paper (hop=0) into the citation, author, and venue graphs.
- **Input**:
  - `outputs/citations.json`
  - `outputs/authors.json`
  - `outputs/venues.json`
  - `outputs/entity_keys.json`
- **Output**:
  - `outputs/citations_updated.json`
  - `outputs/authors_updated.json`
  - `outputs/venues_updated.json`
  - `outputs/entity_keys_updated.json`
- **Run**:
  ```bash
  python paper_details.py
  ```
- Note: Creates `citation-0` for the main paper and links all hop-1 references to it.

### 10. `generate_anomalous_json.py`

- Detects citation anomalies based on low relevance scores and potential author manipulation via SCCs.
- **Input**:
  - `outputs/enriched_papers_with_scores.json`
  - `outputs/suspicious_hop1_only_sccs.json`
  - `outputs/citations_updated.json`
- **Output**:
  - `outputs/anomalous.json`
- **Run**:
  ```bash
  python generate_anomalous_json.py
  ```
- Note: Flags low-relevancy citations and adds `selfCitation` / `citationRing` indicators if authors belong to hop-1 SCCs.

### 11. `author.sus`

- Identifies suspicious citation rings among authors by analyzing author-author graphs.
- **Input**:
  - `outputs/authors_updated.json`
  - `outputs/citations_updated.json`
- **Output**:
  - `outputs/suspicious_sccs.json`
  - `outputs/suspicious_hop1_only_sccs.json`
  - `outputs/scc_details_with_hop1.json`
- **Run**:
  ```bash
  python author.sus
  ```
- Note: Highlights strongly connected components of authors with suspicious citation behaviors, especially if at least one is from hop-1.

### 12. `venue.sus`

- Identifies suspicious venue-level citation clusters based on citation weight and hop status.
- **Input**:
  - `outputs/citations_updated.json`
  - `outputs/venues_updated.json`
- **Output**:
  - `outputs/suspicious_venues.json`
  - `outputs/hop_venues_any.json`
  - `outputs/scc_details_with_hop_any.json`
- **Run**:
  ```bash
  python venue.sus
  ```
- Note: Detects venue-level SCCs where citations suggest manipulation, based on edge weight and inclusion of hop-0 or hop-1 venues.

---

## ▶️ Running the Full Pipeline

1. Place your paper in the root as `test.pdf`.
2. Place all reference PDFs in `reference_papers/`.
3. Create the `outputs/` directory.
4. Run the following in order:

```bash
python extractor.py
python process_references.py
python raw_ref_to_json.py
python summarize.py
python gpt_relevance.py
python cit_locator.py
python second_hop.py
python citation_graph_builder.py
python paper_details.py
python generate_anomalous_json.py
python author.sus
python venue.sus
```

5. Final outputs are in the `outputs/` folder:
   - `citations_updated.json`
   - `authors_updated.json`
   - `venues_updated.json`
   - `anomalous.json`
   - `suspicious_sccs.json`
   - `suspicious_venues.json`
   - And more...

---

## 📜 Notes

- **Internet Required**: GPT, Semantic Scholar, and OpenAlex all require API access.
- **Naming**: PDFs in `reference_papers/` must match citation numbers (e.g., `1.pdf` for `[1]`).
- **Encoding**: All files are UTF-8. Use a compatible editor for viewing or editing.
- **Customization**: If your folder structure is different, adjust the paths in each script accordingly.
