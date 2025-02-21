import re

def extract_references_section(md_content):
    # Regex to find the "References" heading and capture all text until the next heading or EOF
    section_regex = re.compile(
        r'^#+.*?\bReferences?\b.*?$(.*?)(?=^#+|\Z)',
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )
    
    match = section_regex.search(md_content)
    if match:
        return match.group(1).strip()
    return ""


def split_references(references_text):
    """
    Splits the references text into individual reference entries.
    Assumes each reference starts on a new line beginning with '-', '*', or '+'.
    Converts internal newlines in entries to spaces.
    """
    # Regex to split on lines that start with '-', '*', or '+'
    split_pattern = re.compile(r'^[\-\*\+]\s+', re.MULTILINE)
    
    # Split the text using this pattern
    raw_entries = split_pattern.split(references_text)
    
    # Process entries: strip whitespace, replace internal newlines with spaces
    entries = [
        entry.strip().replace('\n', ' ')
        for entry in raw_entries
        if entry.strip()
    ]
    
    return entries


def extract_references_from_md(md_file_path):
    """
    Reads a Markdown file, finds the references section, 
    and splits it into a list of individual reference entries.
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the references section
    references_section = extract_references_section(content)
    if not references_section:
        print("No references section found.")
        return []
    
    # Split into individual references
    references_list = split_references(references_section)
    return references_list


# Modified usage to save to file
if __name__ == "__main__":
    md_file_path = "outputs/test/test.md"  # Your Markdown file
    output_file = "rawreferences.txt"  # Output file name
    
    refs = extract_references_from_md(md_file_path)
    
    if refs:
        # Join references with commas and save to file
        with open(output_file, 'w', encoding='utf-8') as f:
           f.write('\n'.join(refs))
        print(f"Successfully saved {len(refs)} references to {output_file}")
    else:
        print("No references found to save")