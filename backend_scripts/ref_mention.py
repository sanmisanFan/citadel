import re
import json

def extract_reference_numbers(citation_str):
    """
    Extracts individual reference numbers from a citation string.
    For ranges like "2-5", the function expands it into [2, 3, 4, 5].
    """
    content = citation_str.strip("[]").replace(" ", "")
    numbers = []
    parts = content.split(',')
    for part in parts:
        if '-' in part:  # Handle ranges like 2-5
            try:
                start, end = part.split('-')
                start, end = int(start), int(end)
                numbers.extend(list(range(start, end + 1)))
            except ValueError:
                numbers.append(part)
        else:
            try:
                numbers.append(int(part))
            except ValueError:
                numbers.append(part)
    return numbers

def group_references_by_number(md_content):
    """
    Processes the markdown content line by line, finds citations,
    and groups all lines that mention the same reference number together.
    """
    # Regex to match citations like [1], [2-5], [6,7], etc.
    reference_pattern = re.compile(r'\[\d+[,\-\s\d]*\]')
    groups = {}

    for line in md_content.splitlines():
        line_text = line.strip()
        matches = reference_pattern.findall(line)
        if matches:
            unique_matches = list(set(matches))
            for match in unique_matches:
                ref_nums = extract_reference_numbers(match)
                for num in ref_nums:
                    if num not in groups:
                        groups[num] = []
                    groups[num].append(line_text)
    return groups

def extract_references_from_paper(md_file_path, output_json_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    grouped_references = group_references_by_number(content)
    
    # Sort the reference keys in ascending order. Keys are expected to be integers.
    def sort_key(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            return float('inf')
    
    sorted_keys = sorted(grouped_references.keys(), key=sort_key)
    
    output_data = [{"reference": ref, "texts": grouped_references[ref]} for ref in sorted_keys]
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Found {len(output_data)} reference groups saved to {output_json_path}")

# Example usage
if __name__ == "__main__":
    input_md = "outputs/test/test.md"  # Your input markdown file
    output_json = "reference_mentions.json"  # Output file
    extract_references_from_paper(input_md, output_json)
