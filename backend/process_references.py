import re
from pathlib import Path


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


def process_markdown_string(content: str):
    """
    Step 2 of pipeline. Returns in-memory versions of reference_mentions.json and rawreferences.txt.
    """
    # Extract and group reference mentions
    grouped_references = group_references_by_number(content)
    print(grouped_references)

    # Sort the reference keys in ascending order
    def sort_key(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            return float("inf")

    reference_mentions = sorted(grouped_references.keys(), key=sort_key)

    # Extract and split the references section
    references_section = extract_references_section(content)
    if not references_section:
        print("No references section found.")
        return []

    references_list = split_references(references_section)
    return reference_mentions, references_list


def process_markdown_file(md_file_path: Path):
    """
    Reads a Markdown file, extracts reference mentions and the references section,
    and saves the results to a JSON file and a text file.
    """

    # Read the Markdown file
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    process_markdown_string(content)
