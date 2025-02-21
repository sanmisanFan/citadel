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

def normalize_bbox(rect, page_width, page_height):
    """
    Convert a fitz.Rect object to normalized coordinates (0 to 1) relative to page dimensions.
    Returns a dictionary with height, width, x, and y.
    """
    if rect is None:
        return None
    return {
        "height": (rect.y1 - rect.y0) / page_height,
        "width": (rect.x1 - rect.x0) / page_width,
        "x": rect.x0 / page_width,
        "y": rect.y0 / page_height
    }

def extract_pdf_annotations(pdf_path, json_data):
    """
    For each paper entry in the JSON data, process its "reference_mentions" list.
    Search the PDF to locate each mention's text and extract its bounding box.
    Within that text region, find bounding boxes for the citation marker based on ref_id.
    
    Returns a list of dictionaries containing bounding box data.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        sys.exit(1)

    results = []
    for entry in json_data:
        ref_id = entry.get("ref_id")
        if ref_id is None:
            print(f"Warning: Skipping entry with title '{entry.get('title')}' due to missing ref_id.")
            continue
        
        citation_marker = f"[{ref_id}]"  # e.g., "[1]" for ref_id: 1
        mentions = entry.get("reference_mentions", [])
        
        for mention in mentions:
            text = mention.get("text")
            if not text:
                print(f"Warning: No text found in mention for ref_id {ref_id}. Skipping.")
                continue
                
            found = False
            for page_number in range(len(doc)):
                page = doc[page_number]
                page_width = page.rect.width
                page_height = page.rect.height
                
                # Get the bounding box of the mention text
                text_bbox = get_text_bbox(page, text)
                if text_bbox:
                    # Normalize the text bounding box
                    normalized_text_bbox = normalize_bbox(text_bbox, page_width, page_height)
                    
                    # Search for the citation marker within the text region
                    citations_boxes = []
                    citation_rects = page.search_for(citation_marker, clip=text_bbox)
                    if citation_rects:
                        citation_union = citation_rects[0]
                        for r in citation_rects[1:]:
                            citation_union |= r
                        normalized_citation_bbox = normalize_bbox(citation_union, page_width, page_height)
                        citations_boxes.append({"citation": citation_marker, "bbox": normalized_citation_bbox})
                    
                    results.append({
                        "page": page_number + 1,
                        "ref_id": ref_id,
                        "text": text,
                        "text_bbox": normalized_text_bbox,
                        "citations": citations_boxes,
                        "original_text_bbox": text_bbox  # Keep original for annotation
                    })
                    found = True
                    break
            if not found:
                print(f"Warning: Text for ref_id {ref_id} not found in any page: {text[:50]}...")

    doc.close()
    return results

def update_enriched_papers_with_bboxes(enriched_papers, results):
    """
    Update enriched_papers by adding bounding box data to each reference_mentions entry.
    """
    # Create a lookup dictionary for results by text
    results_lookup = {res["text"]: res for res in results}
    
    for paper in enriched_papers:
        mentions = paper.get("reference_mentions", [])
        for mention in mentions:
            text = mention.get("text")
            if text in results_lookup:
                result = results_lookup[text]
                mention["page"] = result["page"]
                mention["text_bbox"] = result["text_bbox"]
                mention["citations"] = result["citations"]
            else:
                mention["page"] = None
                mention["text_bbox"] = None
                mention["citations"] = []
                print(f"Warning: No bounding box data found for text in ref_id {paper.get('ref_id')}: {text[:50]}...")
    
    return enriched_papers

def annotate_pdf(pdf_path, results, output_pdf_path):
    """
    Open the PDF and draw bounding rectangles:
      - The full text bounding box is drawn in blue.
      - The citation bounding boxes are drawn in red.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file for annotation: {e}")
        sys.exit(1)

    for res in results:
        page_number = res["page"] - 1  # Convert to 0-indexed
        page = doc[page_number]

        # Draw the text bounding box (in blue)
        if "original_text_bbox" in res and res["original_text_bbox"]:
            page.draw_rect(res["original_text_bbox"], color=(0, 0, 1), width=2)
        
        # Draw the citation bounding boxes (in red)
        page_width = page.rect.width
        page_height = page.rect.height
        for citation in res["citations"]:
            if citation["bbox"]:
                bbox = citation["bbox"]
                rect = fitz.Rect(
                    bbox["x"] * page_width,
                    bbox["y"] * page_height,
                    (bbox["x"] + bbox["width"]) * page_width,
                    (bbox["y"] + bbox["height"]) * page_height
                )
                page.draw_rect(rect, color=(1, 0, 0), width=2)

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
    json_path = "outputs/enriched_papers_with_scores.json"   # Input JSON file
    output_pdf_path = "annotated_test.pdf"    # Path for the annotated PDF output
    output_json_path = "outputs/annotated_results.json"  # Separate results file
    updated_json_path = "outputs/enriched_papers_with_bboxes.json"  # Updated enriched papers

    # Load the JSON file.
    try:
        with open(json_path, "r") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Extract text and citation bounding boxes from the PDF.
    results = extract_pdf_annotations(pdf_path, json_data)

    # Print out the results with normalized bounding boxes.
    for res in results:
        print(f"Page {res['page']}, Ref ID: {res['ref_id']}")
        print("  Text Bounding Box:", res["text_bbox"])
        for c in res["citations"]:
            print("  Citation:", c["citation"], "Bounding Box:", c["bbox"])

    # Update enriched_papers with bounding box data
    updated_json_data = update_enriched_papers_with_bboxes(json_data, results)

    # Save the updated enriched_papers
    with open(updated_json_path, "w", encoding="utf-8") as f:
        json.dump(updated_json_data, f, indent=2)
    print(f"Updated enriched papers with bounding boxes saved to {updated_json_path}")

    # Annotate and save the PDF with highlighted bounding boxes.
    annotate_pdf(pdf_path, results, output_pdf_path)

    # Save the standalone results with normalized bounding boxes to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as f:
        for res in results:
            res.pop("original_text_bbox", None)  # Remove temporary field
        json.dump(results, f, indent=2)
    print(f"Annotation results saved to {output_json_path}")