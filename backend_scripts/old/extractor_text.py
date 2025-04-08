import re
import sys

def fix_nested_references(match):
    """
    Recursively removes nested brackets inside a reference string and returns a flattened reference.
    Example:
        "[18, [5]]" -> "[18, 5]"
        "[[[16]]]"  -> "[16]"
        "[22, [12]]" -> "[22, 12]"
    """
    inside = match.group(1)
    
    # Recursively remove nested brackets
    while re.search(r'\[([^\[\]]*)\]', inside):
        inside = re.sub(r'\[([^\[\]]*)\]', r'\1', inside)
    
    # Trim extra spaces, commas, and rebuild
    parts = [part.strip() for part in inside.split(',')]
    cleaned_parts = [part for part in parts if part]
    inside = ', '.join(cleaned_parts)
    
    return f'[{inside}]' if inside else ''

def clean_markdown(file_path, output_path):
    """
    Removes:
    1) HTML tags
    2) Standard Markdown inline links [text](url)
    3) Nested bracket references [18, [5]](#page-1-4) -> [18, 5]
    4) Excess backslashes (preserving intentional escapes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 1) Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        print("After HTML removal:", content[:100] + "..." if len(content) > 100 else content)
        
        # 2) Remove standard inline links [text](url) -> text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        print("After link removal:", content[:100] + "..." if len(content) > 100 else content)
        
        # 3) Flatten and retain references while removing link anchors
        # First handle references with anchors: [content](#page-...) 
        content = re.sub(r'\[([^\]]+)\]\(#[^\)]+\)', lambda m: fix_nested_references(m), content)
        
        # Then handle any remaining nested brackets not linked to pages
        nested_bracket_pattern = r'\[([^\]]*\[[^\]]*\][^\]]*)\]'
        while re.search(nested_bracket_pattern, content):
            content = re.sub(nested_bracket_pattern, lambda m: fix_nested_references(m), content)
            
        print("After reference flattening:", content[:100] + "..." if len(content) > 100 else content)
        
        # 4) Fix backslash issues - CORRECTED THIS PART
        # Replace double backslashes with a temporary placeholder
        content = content.replace('\\\\', '##DOUBLESLASH##')
        
        # Replace single unnecessary backslashes
        content = re.sub(r'\\([^\\[\]{}()*+?|^$.#])', r'\1', content)
        
        # Restore double backslashes as single backslashes
        content = content.replace('##DOUBLESLASH##', '\\')
        
        print("After backslash cleanup:", content[:100] + "..." if len(content) > 100 else content)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print(f"Cleaned Markdown file saved to: {output_path}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()  # Print the full stack trace for better debugging

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_markdown.py input.md output.md")
        sys.exit(1)
    else:
        clean_markdown(sys.argv[1], sys.argv[2])