#pip install PyMuPDF
import fitz
import json

# Open the PDF file
doc = fitz.open("reviewerAPP_case1.pdf")

results = []

# --- Handle compound citation on page 2 ---
# On page 2 (index 1), citation [22] appears as part of the compound "[22, 12]".
compound_rects = doc[1].search_for("[22, 12]")
if compound_rects:
    # Take the first occurrence
    compound_rect = compound_rects[0]
    x0, y0, x1, y1 = compound_rect
    compound_width = x1 - x0
    # We assume the compound text "[22, 12]" has 8 characters.
    # We approximate that citation "[22]" occupies the left half.
    citation_x0 = x0
    citation_width = compound_width / 2  # left half of the compound
    # Construct a new rectangle for citation [22]
    bbox_compound = fitz.Rect(citation_x0, y0, citation_x0 + citation_width, y1)
    
    # Normalize relative to page 2 dimensions
    page2_width = doc[1].rect.width
    page2_height = doc[1].rect.height
    norm_bbox_compound = {
        "x": round(bbox_compound.x0 / page2_width, 3),
        "y": round(bbox_compound.y0 / page2_height, 3),
        "width": round(bbox_compound.width / page2_width, 3),
        "height": round(bbox_compound.height / page2_height, 3)
    }
    
    results.append({
        "page": 2,
        "has_issue": False,
        "issues": [],
        "bbox": norm_bbox_compound
    })

# --- Handle direct occurrences of "[22]" on all pages ---
for i in range(doc.page_count):
    page = doc[i]
    rects = page.search_for("[22]")
    for rect in rects:
        # If we're on page 2, skip the direct result if we've already processed compound citation
        if (i + 1) == 2 and results and results[-1]["page"] == 2:
            continue
        page_width = page.rect.width
        page_height = page.rect.height
        norm_bbox = {
            "x": round(rect.x0 / page_width, 3),
            "y": round(rect.y0 / page_height, 3),
            "width": round((rect.x1 - rect.x0) / page_width, 3),
            "height": round((rect.y1 - rect.y0) / page_height, 3)
        }
        results.append({
            "page": i + 1,
            "has_issue": False,
            "issues": [],
            "bbox": norm_bbox
        })

# Print the final JSON output
output = {"cite_positions": results}
print(json.dumps(output, indent=2))
