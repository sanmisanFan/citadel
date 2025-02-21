# Citation Processing Pipeline

This project processes a PDF research paper to extract references, enrich them with metadata, summarize cited papers, assess citation relevance, locate citations in the PDF, fetch second-hop references, and generate structured JSON outputs (citations, authors, venues).

---

## Prerequisites

- Python 3.x  
- Dependencies:  
  ```bash
  pip install requests openai PyPDF2 PyMuPDF nltk marker
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

## Scripts and Execution Order

Below is an overview of each script, its purpose, inputs, and outputs. **Run them in the order listed** to ensure the pipeline functions correctly.

### 1. `extractor.py`
- **Purpose**: Converts `test.pdf` to Markdown and JSON using the `marker` CLI tool, extracting text and structure.  
- **Input**: `test.pdf`  
- **Output**:  
  - `outputs/test/test.md`  
  - `outputs/test/test.json`  
- **Run**:
  ```bash
  python extractor.py
  ```
- **Note**: Ensure `marker` is installed via `pip install marker`.

### 2. `process_references.py`
- **Purpose**: Extracts citation mentions and the references section from the Markdown file, creating grouped mentions and a raw references list.  
- **Input**: `outputs/test/test.md`  
- **Output**:  
  - `outputs/reference_mentions.json`  
  - `outputs/rawreferences.txt`  
- **Run**:
  ```bash
  python process_references.py
  ```
- **Note**: Processes citations like `[1]`, `[2-5]` into structured data.

### 3. `raw_ref_to_json.py`
- **Purpose**: Parses raw references from `rawreferences.txt` with GPT, enriches them with Semantic Scholar and OpenAlex data, and assigns entity keys for hop 1 citations.  
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
- **Note**: Creates initial hop 1 citation data with metadata.

### 4. `summarize.py`
- **Purpose**: Summarizes PDFs of referenced papers stored locally using GPT, assuming filenames match reference numbers (e.g., `1.pdf` for `[1]`).  
- **Input**: `reference_papers/*.pdf`  
- **Output**: `outputs/pdf_summaries.json`  
- **Run**:
  ```bash
  python summarize.py
  ```
- **Note**: Requires PDFs in `reference_papers/` folder.

### 5. `gpt_relevance.py`
- **Purpose**: Assesses citation relevance using GPT, scores mentions, and updates `enriched_papers.json` with relevance data.  
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
- **Note**: Links summaries to citations for relevance scoring.

### 6. `cit_locator.py`
- **Purpose**: Locates citation mentions in `test.pdf`, annotates bounding boxes, and updates `enriched_papers_with_scores.json` with location data.  
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
- **Note**: Adds spatial data to hop 1 citations.

### 7. `second_hop.py`
- **Purpose**: Fetches second-hop citations (references of hop 1 papers) from Semantic Scholar or OpenAlex, updating entity keys with hop 2 data.  
- **Input**:  
  - `outputs/enriched_papers.json`  
  - `outputs/entity_keys.json`  
- **Output**:  
  - `outputs/second_hop_references.json`  
  - Updates `outputs/entity_keys.json`  
- **Run**:
  ```bash
  python second_hop.py
  ```
- **Note**: Adds `"second_hop": "yes"` to hop 2 citations in `entity_keys.json`.

### 8. `citation_graph_builder.py`
- **Purpose**: Combines hop 1 and hop 2 citations into structured JSON files, linking hop 1 to hop 2 via `citation_graph`, ensuring title-based uniqueness.  
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
- **Note**: Produces the final structured output with citation relationships.

---

## Running the Pipeline

1. **Place** `test.pdf` in the root directory.  
2. **Place** reference PDFs in the `reference_papers/` folder.  
3. **Create** an `outputs/` folder.  
4. **Run** the scripts in order:

   ```bash
   python extractor.py
   python process_references.py
   python raw_ref_to_json.py
   python summarize.py
   python gpt_relevance.py
   python cit_locator.py
   python second_hop.py
   python citation_graph_builder.py
   ```

5. Check the `outputs/` folder for results:
   - `citations.json`
   - `authors.json`
   - `venues.json`
   - and intermediate files generated at each step.

---

## Notes

- **Internet Access**: Required for Semantic Scholar, OpenAlex, and OpenAI API calls.  
- **File Paths**: Adjust paths in scripts if your directory structure differs.  
- **Outputs**: All files are UTF-8 encoded; use a compatible editor to view.  
- **Reference PDFs**: Ensure filenames in `reference_papers/` match the reference numbers (e.g., `1.pdf` for `[1]`).
