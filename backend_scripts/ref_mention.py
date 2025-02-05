import re
import json

def find_reference_mentions(md_content):
    # Regex pattern to find reference citations like [1], [2-5], [6,7], etc.
    reference_pattern = re.compile(r'\[\d+[,\-\s\d]*\]')
    
    references = []
    
    for line_num, line in enumerate(md_content.split('\n'), start=1):
        matches = reference_pattern.findall(line)
        if matches:
            # Remove duplicate matches in the same line
            unique_matches = list(set(matches))
            references.append({
                "line_number": line_num,
                "text": line.strip(),
                "citations": unique_matches
            })
    
    return references

def extract_references_from_paper(md_file_path, output_json_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    reference_mentions = find_reference_mentions(content)
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(reference_mentions, f, indent=2)
    
    print(f"Found {len(reference_mentions)} reference mentions saved to {output_json_path}")

# Example usage
if __name__ == "__main__":
    input_md = "outputs/test/test.md"  # Your input markdown file
    output_json = "reference_mentions.json"  # Output file
    
    extract_references_from_paper(input_md, output_json)