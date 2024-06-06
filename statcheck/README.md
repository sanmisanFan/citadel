# PDF Statistical Test Validator

This project converts PDF files to text, extracts statistical test results (F-tests, t-tests, and Chi-square tests), and validates the reported p-values.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Examples](#examples)

## Installation

1. Install the required Python packages:
   ```bash
   pip install scipy pymupdf
   ```

## Usage

To use the script, simply provide the path to a PDF file. The script will extract the text, find statistical tests, and validate the p-values.

# Example usage

pdf_path = 'path/to/your/pdf/p4045.pdf'
process_pdf_file(pdf_path)
