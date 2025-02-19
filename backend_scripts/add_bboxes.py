import json
import re
import fitz  # PyMuPDF

# Define file paths
marker_json_path = "outputs/test/test.json"      # JSON file produced by Marker
pdf_path = "test.pdf"                             # Original PDF file
annotated_pdf_path = "annotated_output.pdf"       # Output PDF with annotations
enriched_json_path = "enriched_papers.json"       # Input enriched papers JSON file
updated_enriched_json_path = "enriched_papers_with_bboxes.json"  # Output JSON with bbox data
debug_log_path = "debug_log.txt"                  # File to store debug information

# Open the debug log file in write mode
debug_file = open(debug_log_path, "w", encoding="utf-8")

def debug(message):
    debug_file.write(message + "\n")

def strip_html(html):
    """Simple function to remove HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", html)

# Load the Marker JSON data (from the Marker tool)
with open(marker_json_path, "r", encoding="utf-8") as f:
    marker_data = json.load(f)

# Check if the marker data is a dict with a "children" key, otherwise assume it's a list
if isinstance(marker_data, dict) and "children" in marker_data:
    marker_pages = marker_data["children"]
else:
    marker_pages = marker_data

# Open the PDF with PyMuPDF
doc = fitz.open(pdf_path)

# Load the enriched papers JSON (each reference should have a "reference_mentions" key with a list of texts)
with open(enriched_json_path, "r", encoding="utf-8") as f:
    enriched_data = json.load(f)

# Process each reference in the enriched data
for ref in enriched_data:
    if "reference_mentions" in ref:
        mentions = ref["reference_mentions"]
        # Prepare a new list to store each mention and its found bounding boxes
        mentions_bboxes = []
        # For each reference mention text
        for mention in mentions:
            # Normalize the mention text by removing any leading dash and extra whitespace
            normalized_mention = mention.lower().lstrip("- ").strip()
            debug(f"DEBUG: Searching for normalized mention text: \"{normalized_mention}\" (original: \"{mention}\")")
            mention_bboxes = []  # List to store bbox info for this mention
            # Search through each page from the Marker JSON
            for page_idx, page_data in enumerate(marker_pages):
                page_found = False
                # Ensure the page data has child blocks
                if "children" in page_data:
                    for block in page_data["children"]:
                        block_html = block.get("html", "")
                        normalized_block = strip_html(block_html).lower()
                        # Log the block text and if it matches the normalized mention
                        match = normalized_mention in normalized_block
                        debug(f"DEBUG: Page {page_idx+1} block: \"{normalized_block}\" - Match: {match}")
                        if match:
                            bbox = block.get("bbox")
                            if bbox and len(bbox) == 4:
                                page_found = True
                                debug(f"DEBUG: Found mention on page {page_idx+1} with bbox: {bbox}")
                                # Record the bounding box along with the page number and the plain block text
                                mention_bboxes.append({
                                    "page": page_idx + 1,
                                    "bbox": bbox,
                                    "block_text": normalized_block
                                })
                                # Annotate the found bbox on the PDF page
                                page = doc[page_idx]
                                rect = fitz.Rect(bbox)
                                annot = page.add_rect_annot(rect)
                                annot.set_colors(stroke=(1, 0, 0))  # red border
                                annot.set_border(width=1)
                                annot.update()
                    if not page_found:
                        debug(f"DEBUG: No match on page {page_idx+1} for normalized mention text: \"{normalized_mention}\"")
            if not mention_bboxes:
                debug(f"DEBUG: No bounding boxes found for mention: \"{normalized_mention}\"")
            mentions_bboxes.append({
                "text": mention,
                "bboxes": mention_bboxes
            })
        # Add the new key to the reference object
        ref["reference_mentions_bboxes"] = mentions_bboxes

# Save the annotated PDF
doc.save(annotated_pdf_path)
debug(f"DEBUG: Annotated PDF saved as {annotated_pdf_path}")

# Save the updated enriched papers JSON with bounding box data
with open(updated_enriched_json_path, "w", encoding="utf-8") as f:
    json.dump(enriched_data, f, indent=2, ensure_ascii=False)
debug(f"DEBUG: Updated enriched papers JSON saved as {updated_enriched_json_path}")

# Close the debug log file
debug_file.close()
print(f"Processing complete. See '{annotated_pdf_path}', '{updated_enriched_json_path}', and '{debug_log_path}' for details.")
