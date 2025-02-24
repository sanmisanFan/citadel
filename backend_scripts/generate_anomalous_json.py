import json
import re
from collections import defaultdict

# Load JSON files
with open('outputs/citations.json', 'r', encoding='utf-8') as f:
    citations_data = json.load(f)["citations"]
with open('outputs/authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)["authors"]
with open('outputs/venues.json', 'r', encoding='utf-8') as f:
    venues_data = json.load(f)["venues"]
with open('outputs/enriched_papers_with_bboxes.json', 'r', encoding='utf-8') as f:
    enriched_papers = json.load(f)
with open('outputs/annotated_results.json', 'r', encoding='utf-8') as f:
    annotated_results = json.load(f)
with open('outputs/statistics.json', 'r', encoding='utf-8') as f:
    stats_data = json.load(f)