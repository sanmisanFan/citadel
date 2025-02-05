# Research Paper Reference Extraction Pipeline

This project provides a structured pipeline to extract, process, and enrich research paper references using various tools, including `marker-pdf`, `Semantic Scholar API`, and `OpenAI`.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- **Python 3.x**
- Required Python packages (install with):
  ```sh
  pip install marker-pdf openai requests
  ```
- **Marker-PDF CLI Tool**: Ensure `marker_single` is accessible.

## Pipeline Overview

This pipeline processes a research paper in the following steps:

1. **Extract text from a PDF** (`extractor.py`)
2. **Extract references from the Markdown output** (`refextract.py`)
3. **Parse references using OpenAI and enrich with Semantic Scholar** (`raw_ref_to_json.py`)
4. **Fetch second-hop references (papers cited by the references)** (`second_hop.py`)

## Steps to Run

### 1. Extract Text from PDF

Run `extractor.py` to extract text from a research paper in **Markdown format**.

```sh
python extractor.py
```

- The extracted output will be saved in the `outputs/` directory.

### 2. Extract References

Run `refextract.py` to extract the **References section** from the generated Markdown file.

```sh
python refextract.py
```

- This script saves extracted references to `rawreferences.txt`.

### 3. Convert References to JSON

Run `raw_ref_to_json.py` to parse references, extract metadata using OpenAI, and enrich details via **Semantic Scholar**.

```sh
python raw_ref_to_json.py
```

- This script generates `output.json`, containing structured reference data.

### 4. Fetch Second-Hop References

Run `second_hop.py` to retrieve citations of the referenced papers.

```sh
python second_hop.py
```

- This script generates `hop2.json`, containing references cited by the original paper's references.

## Output Files

| File                 | Description |
|----------------------|-------------|
| `outputs/test.md`    | Extracted Markdown content from the PDF |
| `rawreferences.txt`  | Extracted references from the Markdown file |
| `output.json`        | JSON representation of parsed references |
| `hop2.json`          | JSON of second-hop references |

## Notes

- Ensure you provide an **API key** for OpenAI in `raw_ref_to_json.py`.
- Rate limits apply for OpenAI and Semantic Scholar APIs; avoid excessive queries.


