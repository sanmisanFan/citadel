import json

# Load the JSON data
with open('outputs/reference_mentions.json', 'r') as f:
    data = json.load(f)

# Create a dictionary to store citations and their corresponding texts
citation_map = {}

# Process each entry in the original data
for entry in data:
    text = entry['text']
    citations = entry['citations']
    
    for citation in citations:
        if citation not in citation_map:
            citation_map[citation] = []
        citation_map[citation].append(text)

# Sort citations numerically by their reference number
sorted_citations = sorted(citation_map.keys(), key=lambda x: int(x.strip('[]')))
sorted_citation_map = {citation: citation_map[citation] for citation in sorted_citations}

# Save the organized data to a new JSON file
with open('organized_citations.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_citation_map, f, indent=2, ensure_ascii=False)

print("Citations organized successfully!")