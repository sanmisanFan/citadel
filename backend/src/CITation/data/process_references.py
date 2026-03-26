import re
from pathlib import Path
from markdown_it import MarkdownIt
import json
from .datatypes import ParsedReference


# TODO: add tests
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


# add test
def extract_references_section(md_content: str) -> list[str]:
    """
    Extracts the "References" section from Markdown content.
    Instead of using regex, uses the markdown-it parser to find a heading with
    the word "references" in it and cleanly only grabs list items.
    """

    md = MarkdownIt()
    tokens = md.parse(md_content)

    refs_start = -1
    refs_level = 0

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])  # "h2" -> 2, etc.

            # The heading text is usually in the next inline token
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                title = tokens[i + 1].content.strip().lower()

                if "reference" in title:
                    refs_start = i
                    refs_level = level
                    break
        i += 1

    if refs_start == -1:
        raise ValueError("References section not found!")

    content_tokens = []
    i = refs_start + 1

    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])
            if level <= refs_level:
                break

        content_tokens.append(token)
        i += 1

    # --- Extract only list item text ---
    references = []
    in_list_item = False

    for token in content_tokens:
        if token.type == "list_item_open":
            in_list_item = True

        elif token.type == "list_item_close":
            in_list_item = False

        elif in_list_item and token.type == "inline":
            text = token.content.strip()
            if text:  # skip empty
                references.append(text)

    return references


def process_markdown_string(content: str):
    """
    Step 2 of pipeline. Returns in-memory versions of reference_mentions.json and rawreferences.txt.
    """
    # Extract and group reference mentions
    grouped_references = group_references_by_number(content)

    # Sort the reference keys in ascending order
    def sort_key(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            return float("inf")

    sorted_grouped_references = {
        key: grouped_references[key]
        for key in sorted(grouped_references.keys(), key=sort_key)
    }

    references_section = extract_references_section(content)

    return sorted_grouped_references, references_section


def process_markdown_file(md_file_path: Path):
    """
    Reads a Markdown file, extracts reference mentions and the references section,
    and saves the results to a JSON file and a text file.
    """

    # Read the Markdown file
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    process_markdown_string(content)


def parse_reference_with_gpt(gpt_client, ref_text: str) -> ParsedReference | None:
    prompt = f"""
Parse this academic reference into JSON format with the following keys: authors (array), title, venue, raw_venue, year, pages, arxiv_id, doi and abstract.
If the venue name in the reference appears abbreviated, expand it to its full name and save the expanded version in "venue",
while preserving the original text in "raw_venue". Use the DOI or axiv link to extract the abstract for the reference. If you are unable to find the abstract using the DOI, search for it using the title in Google Scholar. If you are still unable to find the abstract, leave it as `null`. DO NOT summarize the paper, return only the abstract verbatim. Handle incomplete information using null for missing fields.

Reference: "{ref_text}"

Return JSON only, no commentary.
Example:
{{
  "authors": ["Author 1", "Author 2"],
  "title": "Paper Title",
  "venue": "International Conference on Very Large Data Bases",
  "raw_venue": "VLDB",
  "year": 2023,
  "pages": "123-145",
  "arxiv_id": "1234.5678",
  "doi": "10.1234/abcd",
  "abstract": "Lorem ipsum..."
}}
"""

    try:
        response = gpt_client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type": "web_search"}],
            input=f"{prompt}\n\nReturn ONLY valid JSON as a plain text string without formatting.",
        )
        gpt_output = response.output_text
        print("DEBUG: Received GPT response:", gpt_output)
        result = json.loads(gpt_output)
        if "authors" in result:
            result["authors"] = [
                author for author in result["authors"] if "et al" not in author.lower()
            ]
        return result
    except Exception as e:
        print(f"DEBUG: GPT parsing failed for reference: {ref_text} with error: {e}")
        return None


def parse_references(gpt_client, references: list[str]) -> list[ParsedReference]:
    print(f"DEBUG: Found {len(references)} references in the input file")
    parsed_papers = []
    for idx, ref in enumerate(references, 1):
        print(f"DEBUG: Parsing reference {idx}: {ref}")
        paper_data = parse_reference_with_gpt(gpt_client, ref)
        if paper_data:
            print(f"DEBUG: Successfully parsed reference {idx}")
            paper_data["ref_id"] = idx
            parsed_papers.append(paper_data)
        else:
            print(f"DEBUG: Failed to parse reference {idx}: {ref}")
    return parsed_papers
