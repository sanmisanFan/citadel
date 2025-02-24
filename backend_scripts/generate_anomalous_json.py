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


citation_graph = {c["id"]: c["citation_graph"] for c in citations_data}
out_degree = {c["id"]: len(c["citation_graph"]) for c in citations_data}
in_degree = defaultdict(int)
for c in citations_data:
    for cited in c["citation_graph"]:
        in_degree[cited] += 1
total_citations = sum(out_degree.values())
expected_citations = {}
for citing in out_degree:
    for cited in in_degree:
        expected_citations[(citing, cited)] = (out_degree[citing] * in_degree[cited]) / total_citations


actual_citations = defaultdict(int)
for citing, cited_list in citation_graph.items():
    for cited in cited_list:
        actual_citations[(citing, cited)] += 1

excessive_edges = []
for (citing, cited), actual in actual_citations.items():
    expected = max(1, expected_citations.get((citing, cited), 0))
    if actual > 2 * expected:  # Threshold (adjustable)
        excessive_edges.append((citing, cited, actual, expected))

