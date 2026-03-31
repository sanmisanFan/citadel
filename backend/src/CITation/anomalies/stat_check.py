"""
Statistical test validation for research papers.
Extracts and validates F-tests, t-tests, chi-square tests, and ANOVA results.
"""

import re
from math import isclose
from scipy.stats import t as t_dist, f as f_dist, chi2 as chi2_dist
import fitz  # pymupdf


def pdf_to_plain_text(pdf_bytes):
    """
    Extract plain text directly from PDF bytes.
    This avoids markdown formatting artifacts that interfere with pattern matching.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text


def pdf_to_pages(pdf_bytes):
    """
    Extract plain text from PDF, page by page.
    Returns list of (page_number, text) tuples (1-indexed page numbers).
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append((i + 1, text))  # 1-indexed page numbers
    doc.close()
    return pages


def extract_sentence_context(text, match_start, match_end, context_chars=200):
    """
    Extract the sentence containing a match for highlighting.
    Tries to find sentence boundaries, falls back to character context.
    """
    # Normalize text - replace newlines with spaces for better sentence detection
    # PDF text often has line breaks in the middle of sentences
    normalized_text = text.replace('\n', ' ').replace('\r', ' ')

    # Try to find sentence boundaries
    # Look backwards for sentence start (only real sentence endings, not newlines)
    start = match_start
    while start > 0 and start > match_start - context_chars:
        char = normalized_text[start - 1]
        # Check for sentence end: period/!/?  followed by space and capital, or just period at end
        if char in '.!?':
            # Make sure it's a real sentence end (not abbreviation like "e.g.")
            if start < 2 or normalized_text[start - 2] in ' \t':
                break
        start -= 1

    # Look forwards for sentence end
    end = match_end
    while end < len(normalized_text) and end < match_end + context_chars:
        if normalized_text[end] in '.!?':
            end += 1
            break
        end += 1

    sentence = normalized_text[start:end].strip()
    # Clean up multiple spaces
    sentence = ' '.join(sentence.split())
    # Remove hyphenation from line breaks (e.g., "Fac- tor" -> "Factor")
    sentence = re.sub(r'(\w)-\s+(\w)', r'\1\2', sentence)
    return sentence


def preprocess_text(text):
    """
    Preprocess text for statistical test extraction.
    Based on statcheck's approach for handling PDF encoding issues.
    """
    # Normalize unicode - replace narrow no-break space with regular space
    text = text.replace('\u202f', ' ')
    text = text.replace('\u00a0', ' ')  # non-breaking space

    # Fix common PDF encoding errors (based on statcheck)
    # Sometimes 'b' is misread as '<', 'N' as '>', 'p' as '='
    # We handle this more conservatively - only in statistical contexts

    # Fix minus signs - various unicode dashes to regular minus
    text = text.replace('−', '-')  # unicode minus
    text = text.replace('–', '-')  # en dash
    text = text.replace('—', '-')  # em dash

    # Remove thousand separators in numbers (e.g., 1,000 -> 1000)
    text = re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', text)

    # Normalize whitespace around statistical notation
    # Fix cases like "F (2, 46)" -> "F(2,46)"
    text = re.sub(r'([FtTrRzZ])\s*\(\s*', r'\1(', text)
    text = re.sub(r'\s*,\s*', ',', text)
    text = re.sub(r'\s*\)', ')', text)

    # Fix spaced decimals: ". 01" -> ".01"
    text = re.sub(r'\.\s+(\d)', r'.\1', text)

    # Fix spaced comparisons: "p < . 01" -> "p <.01", "= 4" -> "=4"
    text = re.sub(r'([<>=])\s+', r'\1', text)
    text = re.sub(r'\s+([<>=])', r' \1', text)

    # Collapse multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize p-value notation
    text = re.sub(r'[pP]\s*[<>=]', lambda m: m.group().replace(' ', ''), text)

    return text


def parse_number(s):
    """Safely parse a number string."""
    if not s:
        return None
    s = s.strip().lstrip('=')
    if not s:
        return None
    if s.startswith('.'):
        s = '0' + s
    try:
        return float(s)
    except ValueError:
        return None


def round_to_reported(computed_p, reported_p):
    """Round computed p-value to same decimal places as reported."""
    try:
        decimal_places = len(str(reported_p).split(".")[1])
        return round(computed_p, decimal_places)
    except (IndexError, ValueError):
        return round(computed_p, 3)


# Regex patterns for different test formats
# Note: Using (\d*\.?\d+) to match numbers with optional decimal, avoids trailing periods
# df values can be decimal (e.g., Greenhouse-Geisser corrected ANOVA)
PATTERNS = {
    # F-test patterns: F(df1, df2) = value, p < value
    'f_test': [
        re.compile(r'[fF]\s*[\(\[]\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\s*[\)\]]\s*=\s*(\d*\.?\d+)\s*[,;]?\s*[pP]\s*([<>=])\s*(\d*\.?\d+)', re.IGNORECASE),
        re.compile(r'_F_\s*\(\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\s*\)\s*=\s*(\d*\.?\d+)[^_]*_p_\s*([<>=]+)\s*(\d*\.?\d+)', re.IGNORECASE),
    ],
    # t-test patterns: t(df) = value, p < value
    't_test': [
        re.compile(r'[tT]\s*[\(\[]\s*(\d*\.?\d+)\s*[\)\]]\s*=\s*([+-]?\d*\.?\d+)\s*[,;]?\s*[pP]\s*([<>=])\s*(\d*\.?\d+)', re.IGNORECASE),
        re.compile(r'_t_\s*\(\s*(\d*\.?\d+)\s*\)\s*=\s*([+-]?\d*\.?\d+)[^_]*_p_\s*([<>=]+)\s*(\d*\.?\d+)', re.IGNORECASE),
    ],
    # Chi-square patterns: χ²(df) = value, p < value
    'chi_square': [
        re.compile(r'[Xxχ]\s*(?:²|\^2|2)?\s*[\(\[]\s*(\d*\.?\d+)\s*(?:,\s*[Nn]\s*=\s*\d+)?\s*[\)\]]\s*=\s*(\d*\.?\d+)\s*[,;]?\s*[pP]\s*([<>=])\s*(\d*\.?\d+)', re.IGNORECASE),
    ],
    # Correlation: r = value, p < value
    'correlation': [
        re.compile(r'[rR]\s*=\s*([+-]?\d*\.?\d+)\s*[,;]?\s*[pP]\s*([<>=])\s*(\d*\.?\d+)', re.IGNORECASE),
    ],
}


def find_all_tests(text):
    """Find all statistical tests in text."""
    results = {
        'f_tests': [],
        't_tests': [],
        'chi_square_tests': [],
        'correlations': [],
    }

    for pattern in PATTERNS['f_test']:
        for match in pattern.findall(text):
            results['f_tests'].append(match)

    for pattern in PATTERNS['t_test']:
        for match in pattern.findall(text):
            results['t_tests'].append(match)

    for pattern in PATTERNS['chi_square']:
        for match in pattern.findall(text):
            results['chi_square_tests'].append(match)

    for pattern in PATTERNS['correlation']:
        for match in pattern.findall(text):
            results['correlations'].append(match)

    return results


def validate_f_test(df1, df2, f_value, p_operator, reported_p, tolerance=0.01):
    """Validate an F-test result."""
    errors = []

    if df1 <= 0 or df2 <= 0:
        errors.append(f"Invalid degrees of freedom: df1={df1}, df2={df2}")
        return False, errors, None

    if f_value < 0:
        errors.append(f"F-value cannot be negative: {f_value}")
        return False, errors, None

    if not (0 <= reported_p <= 1):
        errors.append(f"P-value must be between 0 and 1: {reported_p}")
        return False, errors, None

    # Compute p-value
    computed_p = 1 - f_dist.cdf(f_value, df1, df2)

    # Check consistency
    is_valid = True
    if p_operator == '=':
        if not isclose(computed_p, reported_p, abs_tol=tolerance):
            is_valid = False
            errors.append(f"Reported p={reported_p} doesn't match computed p={computed_p:.4f}")
    elif p_operator == '<':
        if not (computed_p < reported_p + tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not < {reported_p}")
    elif p_operator == '>':
        if not (computed_p > reported_p - tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not > {reported_p}")

    return is_valid, errors, computed_p


def validate_t_test(df, t_value, p_operator, reported_p, tolerance=0.01):
    """Validate a t-test result (two-tailed)."""
    errors = []

    if df <= 0:
        errors.append(f"Invalid degrees of freedom: df={df}")
        return False, errors, None

    if not (0 <= reported_p <= 1):
        errors.append(f"P-value must be between 0 and 1: {reported_p}")
        return False, errors, None

    # Compute two-tailed p-value
    computed_p = 2 * (1 - t_dist.cdf(abs(t_value), df))

    # Check consistency
    is_valid = True
    if p_operator == '=':
        if not isclose(computed_p, reported_p, abs_tol=tolerance):
            is_valid = False
            errors.append(f"Reported p={reported_p} doesn't match computed p={computed_p:.4f}")
    elif p_operator == '<':
        if not (computed_p < reported_p + tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not < {reported_p}")
    elif p_operator == '>':
        if not (computed_p > reported_p - tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not > {reported_p}")

    return is_valid, errors, computed_p


def validate_chi_square(df, chi_value, p_operator, reported_p, tolerance=0.01):
    """Validate a chi-square test result."""
    errors = []

    if df <= 0:
        errors.append(f"Invalid degrees of freedom: df={df}")
        return False, errors, None

    if chi_value < 0:
        errors.append(f"Chi-square value cannot be negative: {chi_value}")
        return False, errors, None

    if not (0 <= reported_p <= 1):
        errors.append(f"P-value must be between 0 and 1: {reported_p}")
        return False, errors, None

    # Compute p-value
    computed_p = 1 - chi2_dist.cdf(chi_value, df)

    # Check consistency
    is_valid = True
    if p_operator == '=':
        if not isclose(computed_p, reported_p, abs_tol=tolerance):
            is_valid = False
            errors.append(f"Reported p={reported_p} doesn't match computed p={computed_p:.4f}")
    elif p_operator == '<':
        if not (computed_p < reported_p + tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not < {reported_p}")
    elif p_operator == '>':
        if not (computed_p > reported_p - tolerance):
            is_valid = False
            errors.append(f"Computed p={computed_p:.4f} is not > {reported_p}")

    return is_valid, errors, computed_p


def extract_context(text, match_str, context_chars=100):
    """Extract surrounding context for a statistical test mention."""
    idx = text.find(match_str)
    if idx == -1:
        return match_str
    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(match_str) + context_chars)
    context = text[start:end]
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    return context


def validate_statistics_in_text(text, tolerance=0.01):
    """
    Validate all statistical tests found in text.

    Returns:
        List of anomaly dictionaries for invalid tests.
    """
    # Preprocess text to handle encoding issues
    text = preprocess_text(text)

    anomalies = []
    tests = find_all_tests(text)
    issue_counter = 1

    # Validate F-tests
    for match in tests['f_tests']:
        if len(match) == 5:
            df1_str, df2_str, f_val_str, p_op, p_val_str = match
        else:
            continue

        df1 = parse_number(df1_str)
        df2 = parse_number(df2_str)
        f_val = parse_number(f_val_str)
        p_val = parse_number(p_val_str)

        if df1 is None or df2 is None or f_val is None or p_val is None:
            continue

        is_valid, errors, computed_p = validate_f_test(df1, df2, f_val, p_op, p_val, tolerance)

        if not is_valid:
            test_str = f"F({df1}, {df2}) = {f_val}, p {p_op} {p_val}"
            anomalies.append({
                "test_type": "F-test (ANOVA)",
                "reported": test_str,
                "errors": errors,
                "computed_p": computed_p,
                "sentence": test_str,
            })

    # Validate t-tests
    for match in tests['t_tests']:
        if len(match) == 4:
            df_str, t_val_str, p_op, p_val_str = match
        else:
            continue

        df = parse_number(df_str)
        t_val = parse_number(t_val_str)
        p_val = parse_number(p_val_str)

        if df is None or t_val is None or p_val is None:
            continue

        is_valid, errors, computed_p = validate_t_test(df, t_val, p_op, p_val, tolerance)

        if not is_valid:
            test_str = f"t({df}) = {t_val}, p {p_op} {p_val}"
            anomalies.append({
                "test_type": "t-test",
                "reported": test_str,
                "errors": errors,
                "computed_p": computed_p,
                "sentence": test_str,
            })

    # Validate chi-square tests
    for match in tests['chi_square_tests']:
        if len(match) == 4:
            df_str, chi_val_str, p_op, p_val_str = match
        else:
            continue

        df = parse_number(df_str)
        chi_val = parse_number(chi_val_str)
        p_val = parse_number(p_val_str)

        if df is None or chi_val is None or p_val is None:
            continue

        is_valid, errors, computed_p = validate_chi_square(df, chi_val, p_op, p_val, tolerance)

        if not is_valid:
            test_str = f"χ²({df}) = {chi_val}, p {p_op} {p_val}"
            anomalies.append({
                "test_type": "Chi-square test",
                "reported": test_str,
                "errors": errors,
                "computed_p": computed_p,
                "sentence": test_str,
            })

    return anomalies


def find_tests_with_positions(text):
    """
    Find all statistical tests in text with their positions.
    Returns list of (match_obj, test_type, groups) tuples.
    """
    results = []

    for pattern in PATTERNS['f_test']:
        for match in pattern.finditer(text):
            results.append((match, 'f_test', match.groups()))

    for pattern in PATTERNS['t_test']:
        for match in pattern.finditer(text):
            results.append((match, 't_test', match.groups()))

    for pattern in PATTERNS['chi_square']:
        for match in pattern.finditer(text):
            results.append((match, 'chi_square', match.groups()))

    return results


def find_matching_coordinate(test_text, formula_coords, page_num):
    """
    Find GROBID coordinates that match a statistical test.

    Args:
        test_text: The statistical test string (e.g., "F(2,46) = 4, p < .01")
        formula_coords: List of GROBID formula coordinates
        page_num: Page number to match

    Returns:
        dict with x, y, width, height, page_height or None if not found
    """
    if not formula_coords:
        return None

    # Normalize for comparison - keep key parts
    def normalize(s):
        s = s.lower()
        s = re.sub(r'\s+', '', s)  # remove spaces
        s = s.replace('.', '')  # remove dots for comparison
        return s

    # Extract key identifying parts from the test text
    # For F(2,46)=4,p<.01, extract f(2,46) and the specific values
    test_normalized = normalize(test_text)

    # Extract the test signature (e.g., "f(2,46)" or "f(047,173)")
    test_signature_match = re.search(r'[ft]\([^)]+\)', test_normalized)
    test_signature = test_signature_match.group(0) if test_signature_match else None

    print(f"DEBUG find_matching: Looking for '{test_text}' on page {page_num}")
    print(f"DEBUG find_matching: Test signature: {test_signature}")

    best_match = None
    best_score = 0

    for coord in formula_coords:
        if coord.get("page") != page_num:
            continue

        coord_text = coord.get("text", "")
        coord_normalized = normalize(coord_text)

        # Check if this coordinate contains a matching signature
        if test_signature and test_signature in coord_normalized:
            # Calculate match score based on how much of our test is in the coord text
            score = len(test_normalized) if test_normalized in coord_normalized else len(test_signature)

            print(f"DEBUG find_matching: Candidate '{coord_text[:50]}...' score={score}")

            if score > best_score:
                best_score = score
                best_match = {
                    "x": coord["x"],
                    "y": coord["y"],
                    "width": coord["width"],
                    "height": coord["height"],
                }

    if best_match:
        print(f"DEBUG find_matching: Best match found with score {best_score}")
    else:
        print(f"DEBUG find_matching: No match found for '{test_text}'")
        # Print available coords on this page for debugging
        page_coords = [c for c in formula_coords if c.get("page") == page_num]
        print(f"DEBUG find_matching: Available coords on page {page_num}: {len(page_coords)}")
        for c in page_coords[:5]:  # Print first 5
            print(f"  - '{c.get('text', '')[:60]}...'")

    return best_match


def generate_statistical_anomalies(pdf_bytes, start_issue_id=1, tolerance=0.01, formula_coords=None):
    """
    Generate anomaly objects for invalid statistical tests.

    Args:
        pdf_bytes: Raw PDF bytes to extract text from
        start_issue_id: Starting ID for issues
        tolerance: Tolerance for p-value comparison
        formula_coords: Optional list of GROBID formula coordinates for exact bbox

    Returns:
        List of anomaly dictionaries compatible with the frontend
    """
    # Extract text page by page
    pages = pdf_to_pages(pdf_bytes)
    issues = []
    issue_id = start_issue_id

    for page_num, raw_text in pages:
        # Preprocess the page text
        text = preprocess_text(raw_text)

        # Find all tests with positions on this page
        test_matches = find_tests_with_positions(text)

        for match, test_type, groups in test_matches:
            # Validate based on test type
            is_valid = True
            errors = []
            computed_p = None
            test_str = ""

            if test_type == 'f_test' and len(groups) == 5:
                df1_str, df2_str, f_val_str, p_op, p_val_str = groups
                df1 = parse_number(df1_str)
                df2 = parse_number(df2_str)
                f_val = parse_number(f_val_str)
                p_val = parse_number(p_val_str)

                if df1 is None or df2 is None or f_val is None or p_val is None:
                    continue

                is_valid, errors, computed_p = validate_f_test(df1, df2, f_val, p_op, p_val, tolerance)
                test_str = f"F({df1},{df2})={f_val}, p{p_op}{p_val}"
                test_type_name = "F-test (ANOVA)"

            elif test_type == 't_test' and len(groups) == 4:
                df_str, t_val_str, p_op, p_val_str = groups
                df = parse_number(df_str)
                t_val = parse_number(t_val_str)
                p_val = parse_number(p_val_str)

                if df is None or t_val is None or p_val is None:
                    continue

                is_valid, errors, computed_p = validate_t_test(df, t_val, p_op, p_val, tolerance)
                test_str = f"t({df})={t_val}, p{p_op}{p_val}"
                test_type_name = "t-test"

            elif test_type == 'chi_square' and len(groups) == 4:
                df_str, chi_val_str, p_op, p_val_str = groups
                df = parse_number(df_str)
                chi_val = parse_number(chi_val_str)
                p_val = parse_number(p_val_str)

                if df is None or chi_val is None or p_val is None:
                    continue

                is_valid, errors, computed_p = validate_chi_square(df, chi_val, p_op, p_val, tolerance)
                test_str = f"χ²({df})={chi_val}, p{p_op}{p_val}"
                test_type_name = "Chi-square test"
            else:
                continue

            if not is_valid:
                # Find the exact stat test in raw text for highlighting
                # Build a flexible pattern to match the test with original spacing
                if test_type == 'f_test':
                    raw_pattern = rf'F\s*\(\s*{re.escape(df1_str)}\s*,\s*{re.escape(df2_str)}\s*\)\s*=\s*[\d.]+\s*,?\s*p\s*[<>=]\s*[\d.]+'
                elif test_type == 't_test':
                    raw_pattern = rf't\s*\(\s*{re.escape(df_str)}\s*\)\s*=\s*[+-]?[\d.]+\s*,?\s*p\s*[<>=]\s*[\d.]+'
                elif test_type == 'chi_square':
                    raw_pattern = rf'[χXx]\s*[²2]?\s*\(\s*{re.escape(df_str)}\s*\)\s*=\s*[\d.]+\s*,?\s*p\s*[<>=]\s*[\d.]+'
                else:
                    raw_pattern = None

                # Use the matched stat test itself for highlighting (simpler, more reliable)
                sentence = test_str  # fallback
                if raw_pattern:
                    raw_match = re.search(raw_pattern, raw_text, re.IGNORECASE)
                    if raw_match:
                        # Use exact matched text from PDF for highlighting
                        sentence = raw_match.group(0).replace('\n', ' ').strip()
                        print(f"DEBUG stat_check: Found in raw text: {repr(sentence)}")
                    else:
                        print(f"DEBUG stat_check: Pattern not found in raw text, using fallback: {test_str}")
                        print(f"DEBUG stat_check: Pattern was: {raw_pattern}")
                        print(f"DEBUG stat_check: Raw text sample: {repr(raw_text[:500])}")

                # Try to get GROBID coordinates for precise positioning
                bbox = find_matching_coordinate(sentence, formula_coords, page_num)
                if bbox:
                    print(f"DEBUG stat_check: Found GROBID bbox for '{sentence}': {bbox}")
                else:
                    print(f"DEBUG stat_check: No GROBID bbox found for '{sentence}' on page {page_num}")

                issue = {
                    "id": f"issue-stat-{issue_id}",
                    "name": "statistic",
                    "displayName": "Statistical Anomaly",
                    "category": {
                        "name": "testFailure",
                        "displayName": "Test Failure",
                        "options": {},
                    },
                    "paper": [],
                    "page": page_num,
                    "explanation": (
                        f"{test_type_name} validation failed.\n"
                        f"Reported: {test_str}\n"
                        f"Issues: {'; '.join(errors)}"
                    ),
                    "sentence": [{"sentence": sentence, "bbox": bbox}],
                }
                issues.append(issue)
                issue_id += 1

    return issues
