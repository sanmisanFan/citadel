import sys
import os

import fitz
import flor


def convert_pdf_to_text(pdf_path):
    """
    Converts a PDF file to text with proper formatting.

    Parameters:
    - pdf_path (str): Path to the PDF file.

    Returns:
    - formatted_text (str): The extracted text from the PDF.
    """
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        # Loop through pages in the PDF
        for page_number, page in flor.loop("page", enumerate(doc)):
            # Extract text from the page
            text = page.get_text()
            flor.log("page_text", text)


if __name__ == "__main__":
    for pdf_path in flor.loop("paper", sys.argv[1:]):
        assert os.path.exists(pdf_path), f"File not found: {pdf_path}"
        assert pdf_path.endswith(".pdf"), f"Invalid file format: {pdf_path}"
        convert_pdf_to_text(pdf_path)
