# Research Paper Reference Extraction Pipeline

This project provides a structured pipeline to extract, process, and enrich research paper references using various tools, including `marker-pdf`, `Semantic Scholar API`, and `OpenAI`.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- **Python 3.x**
- Required Python packages (install with):
  ```sh
  pip install marker-pdf openai requests pymupdf nltk
  ```
- **Marker-PDF CLI Tool**: Ensure `marker_single` is accessible.

## Pipeline Overview

This pipeline processes a research paper in the following steps:

1. **Extract text from a PDF** (`extractor.py`)
2. **Find reference mentions in the text** (`ref_mention.py`)
3. **Extract references from the Markdown output** (`refextract.py`)
4. **Locate citations in the original PDF** (`cit_locator.py`)
5. **Parse references using OpenAI and enrich with Semantic Scholar** (`raw_ref_to_json.py`)
6. **Fetch second-hop references (papers cited by the references)** (`second_hop.py`)

## Steps to Run

### 1. Extract Text from PDF

Run `extractor.py` to extract text from a research paper in **Markdown format**.

```sh
python extractor.py
```

- The extracted output will be saved in the `outputs/` directory.

### 2. Identify Reference Mentions

Run `ref_mention.py` to find reference markers (e.g., `[1]`, `[2-5]`) in the extracted text.

```sh
python ref_mention.py
```

- This script saves reference mentions to `reference_mentions.json`.

### 3. Extract References

Run `refextract.py` to extract the **References section** from the generated Markdown file.

```sh
python refextract.py
```

- This script saves extracted references to `rawreferences.txt`.

### 4. Locate Citations in PDF

Run `cit_locator.py` to find citation bounding boxes in the original PDF and highlight them.

```sh
python cit_locator.py
```

- This script generates `annotated_test.pdf` with highlighted citation mentions.

### 5. Convert References to JSON

Run `raw_ref_to_json.py` to parse references, extract metadata using OpenAI, and enrich details via **Semantic Scholar**.

```sh
python raw_ref_to_json.py
```

- This script generates `output.json`, containing structured reference data.

### 6. Fetch Second-Hop References

Run `second_hop.py` to retrieve citations of the referenced papers.

```sh
python second_hop.py
```

- This script generates `hop2.json`, containing references cited by the original paper's references.

## Output Files

| File                 | Description |
|----------------------|-------------|
| `outputs/test.md`    | Extracted Markdown content from the PDF |
| `reference_mentions.json`  | Identified reference mentions in text |
| `rawreferences.txt`  | Extracted references from the Markdown file |
| `output.json`        | JSON representation of parsed references |
| `hop2.json`          | JSON of second-hop references |
| `annotated_test.pdf` | PDF with highlighted citation bounding boxes |

## Notes

- Ensure you provide an **API key** for OpenAI in `raw_ref_to_json.py`.




