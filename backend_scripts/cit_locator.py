import fitz  # PyMuPDF
import json
import nltk
import sys

# Download required NLTK data packages if they are not already installed.
nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab/english')
except LookupError:
    nltk.download('punkt_tab')


def get_text_bbox(page, text):
    """
    Tokenize the provided text into sentences and search the page for each sentence.
    Combine (union) all found sentence bounding boxes into one bounding rectangle.
    If nothing is found, return None.
    """
    sentences = nltk.tokenize.sent_tokenize(text)
    union_rect = None
    for sentence in sentences:
        # Search for the sentence on the page
        sentence_rects = page.search_for(sentence)
        if sentence_rects:
            # In case the sentence spans multiple parts, combine them.
            sentence_union = sentence_rects[0]
            for r in sentence_rects[1:]:
                sentence_union |= r  # Union of rectangles
            # Combine with the union of previously found sentences
            if union_rect is None:
                union_rect = sentence_union
            else:
                union_rect |= sentence_union
    return union_rect


def extract_pdf_annotations(pdf_path, json_data):
    """
    For each entry in the JSON data (which contains "line_number", "text", and "citations"),
    search the PDF to locate the text and extract its bounding box. Within that text region,
    also find the bounding boxes for each citation marker.
    
    Returns a list of dictionaries containing:
      - page: page number (1-indexed) where the text was found,
      - line_number: from the JSON entry,
      - text: the entry's text,
      - text_bbox: the bounding box (a fitz.Rect) for the full text,
      - citations: a list of dictionaries with each citation marker and its bounding box.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        sys.exit(1)

    results = []
    for entry in json_data:
        found = False
        for page_number in range(len(doc)):
            page = doc[page_number]
            # Try to get the bounding box of the entire text (by combining sentence boxes)
            text_bbox = get_text_bbox(page, entry["text"])
            if text_bbox:
                # Within the found text region, search for each citation marker.
                citations_boxes = []
                for citation in entry.get("citations", []):
                    # Use the clip argument to search only within the text region.
                    citation_rects = page.search_for(citation, clip=text_bbox)
                    if citation_rects:
                        # Combine if the citation is found in several parts.
                        citation_union = citation_rects[0]
                        for r in citation_rects[1:]:
                            citation_union |= r
                        citations_boxes.append({"citation": citation, "bbox": citation_union})
                results.append({
                    "page": page_number + 1,  # converting to 1-indexed page numbers
                    "line_number": entry.get("line_number"),
                    "text": entry["text"],
                    "text_bbox": text_bbox,
                    "citations": citations_boxes
                })
                found = True
                break  # Assume each JSON entry appears on a single page
        if not found:
            print(f"Warning: Text for line {entry.get('line_number')} not found in any page.")
    doc.close()
    return results


def annotate_pdf(pdf_path, results, output_pdf_path):
    """
    Open the PDF and draw bounding rectangles:
      - The full text bounding box is drawn in blue.
      - The citation bounding boxes are drawn in red.
    Save the annotated PDF to output_pdf_path.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file for annotation: {e}")
        sys.exit(1)

    for res in results:
        page_number = res["page"] - 1  # Convert to 0-indexed
        page = doc[page_number]

        # Draw the text bounding box (in blue).
        if res["text_bbox"]:
            page.draw_rect(res["text_bbox"], color=(0, 0, 1), width=2)
        # Draw the citation bounding boxes (in red).
        for citation in res["citations"]:
            if citation["bbox"]:
                page.draw_rect(citation["bbox"], color=(1, 0, 0), width=2)

    try:
        doc.save(output_pdf_path)
        print(f"Annotated PDF saved as {output_pdf_path}")
    except Exception as e:
        print(f"Error saving annotated PDF: {e}")
    finally:
        doc.close()


if __name__ == "__main__":
    # Define your file paths.
    pdf_path = "test.pdf"                   # Path to your PDF file
    json_path = "outputs/reference_mentions.json"   # Path to your JSON file (new format)
    output_pdf_path = "annotated_test.pdf"    # Path for the annotated PDF output

    # Load the JSON file.
    try:
        with open(json_path, "r") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Extract text and citation bounding boxes from the PDF using the JSON data.
    results = extract_pdf_annotations(pdf_path, json_data)

    # Print out the results.
    for res in results:
        print(f"Page {res['page']}, Line Number: {res['line_number']}")
        print("  Text Bounding Box:", res["text_bbox"])
        for c in res["citations"]:
            print("  Citation:", c["citation"], "Bounding Box:", c["bbox"])

    # Annotate and save the PDF with the highlighted bounding boxes.
    annotate_pdf(pdf_path, results, output_pdf_path)
