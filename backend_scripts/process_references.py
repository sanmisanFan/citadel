import os
import re
import json
import flor


def extract_reference_numbers(citation_str):
    """
    Extracts individual reference numbers from a citation string.
    For ranges like "2-5", the function expands it into [2, 3, 4, 5].
    """
    content = citation_str.strip("[]").replace(" ", "")
    numbers = []
    parts = content.split(",")
    for part in parts:
        if "-" in part:  # Handle ranges like 2-5
            try:
                start, end = part.split("-")
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
    reference_pattern = re.compile(r"\[\d+(?:[,\s]*\d+)*(?:[,\s]*\d+-\d+)*\]")
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


def extract_references_section(md_content):
    """
    Extracts the "References" section from Markdown content.
    """
    section_regex = re.compile(
        r"^#+.*?\bReferences?\b.*?$(.*?)(?=^#+|\Z)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE,
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
    split_pattern = re.compile(r"^[\-\*\+]\s+", re.MULTILINE)
    raw_entries = split_pattern.split(references_text)
    entries = [
        entry.strip().replace("\n", " ") for entry in raw_entries if entry.strip()
    ]
    return entries


def process_markdown_file(md_file_path):
    """
    Reads a Markdown file, extracts reference mentions and the references section,
    and saves the results to a JSON file and a text file.
    """

    print(md_file_path)
    import sys

    sys.exit(0)

    # Read the Markdown file
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract and group reference mentions
    grouped_references = group_references_by_number(content)

    # Sort the reference keys in ascending order
    def sort_key(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            return float("inf")

    sorted_keys = sorted(grouped_references.keys(), key=sort_key)
    output_data = [
        {"reference": ref, "texts": grouped_references[ref]} for ref in sorted_keys
    ]

    # Save grouped references to JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"Found {len(output_data)} reference groups saved to {output_json_path}")

    # Extract and split the references section
    references_section = extract_references_section(content)
    if not references_section:
        print("No references section found.")
        references_list = []
    else:
        references_list = split_references(references_section)

    # Save references to text file
    if references_list:
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(references_list))
        print(
            f"Successfully saved {len(references_list)} references to {output_txt_path}"
        )
    else:
        print("No references found to save")


# Example usage
if __name__ == "__main__":
    # listdir in
    root = flor.arg("read_dir", default="outputs/")
    documents = [
        each
        for each in os.listdir(root)
        if os.path.isdir(os.path.join(root, each))
        and os.path.exists(os.path.join(root, each, f"{each}.md"))
    ]
    for doc in flor.loop("document", documents):
        # md_file = "outputs/test/test.md"  # Your input Markdown file
        md_file = os.path.join(root, doc, f"{doc}.md")
        process_markdown_file(md_file)
