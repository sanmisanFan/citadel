import re
from math import isclose

# We will use these for validating t and F distributions.
# Make sure you have installed scipy (e.g., "pip install scipy").
from scipy.stats import t as t_dist, f as f_dist

def parse_number(s):
    """
    Safely parse a number string (which may start with '=' or '.').
    Returns None if parsing fails.
    """
    s = s.strip().lstrip('=')
    if not s:
        return None
    if s.startswith('.'):
        s = '0' + s
    try:
        return float(s)
    except ValueError:
        return None


def validate_statistics(md_content, tolerance=1e-3):
    """
    Searches the given Markdown text for:
       - F-tests formatted like: _F_(df1, df2) = <value>, p <op> <value>
       - t-tests formatted like: _t_(df) = <value>, p <op> <value>
    
    For each match, it verifies:
       1. Degrees of freedom are positive integers.
       2. Test statistic is valid (not None, not negative for F).
       3. Reported p-value is in [0, 1].
       4. The reported p-value is consistent with a library-computed p-value
          (within the given tolerance if p-value uses '='; otherwise it
          checks < or > relationships).
    
    Parameters:
    -----------
    md_content : str
        The Markdown text to be validated.
    tolerance : float
        Numeric tolerance for checking equality of reported vs. computed p-values.
    """
    
    # Regex patterns to capture F(...) = X, p <op> Y  and  t(...) = X, p <op> Y
    f_pattern = re.compile(
        r'_F_\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*=\s*([0-9.]+)(?:[^_]*_p_\s*([<>=]+)\s*([0-9.]+))?',
        re.IGNORECASE
    )
    t_pattern = re.compile(
        r'_t_\s*\(\s*(\d+)\s*\)\s*=\s*([+-]?[0-9.]+)(?:[^_]*_p_\s*([<>=]+)\s*([0-9.]+))?',
        re.IGNORECASE
    )

    print("Statistical Test Validation Results:\n")
    
    # Validate F-tests
    for match in f_pattern.findall(md_content):
        df1_str, df2_str, f_val_str, p_op, p_val_str = match
        valid = True
        errors = []
        
        # Validate degrees of freedom
        if not df1_str.isdigit() or int(df1_str) <= 0:
            valid = False
            errors.append(f"Invalid DF1: {df1_str}")
        if not df2_str.isdigit() or int(df2_str) <= 0:
            valid = False
            errors.append(f"Invalid DF2: {df2_str}")
        
        # Convert DF strings to integers
        df1 = int(df1_str) if df1_str.isdigit() else None
        df2 = int(df2_str) if df2_str.isdigit() else None

        # Validate F-value
        f_val = parse_number(f_val_str)
        if f_val is None or f_val < 0:
            valid = False
            errors.append(f"Invalid F-value: {f_val_str}")
        
        # Validate p-value components
        p_val = parse_number(p_val_str) if p_val_str else None
        if not p_op or not p_val_str:
            valid = False
            errors.append("Missing p-value operator or value")
        elif p_val is None or not (0 <= p_val <= 1):
            valid = False
            errors.append(f"Invalid p-value: {p_val_str}")

        # If all structural checks pass, attempt to verify the p-value with library
        if valid and (f_val is not None) and (df1 is not None) and (df2 is not None):
            # Compute the right-tailed p-value for an F-test
            lib_p = 1 - f_dist.cdf(f_val, df1, df2)
            
            # Compare with p_val according to p_op
            if p_op == '=':
                # Check that they are close within some tolerance
                if not isclose(lib_p, p_val, abs_tol=tolerance):
                    valid = False
                    errors.append(
                        f"Reported p={p_val_str} does not match computed p={lib_p:.5g} (within ±{tolerance})"
                    )
            elif p_op == '<':
                # Verify library p is strictly less than reported p (with some tolerance)
                if not (lib_p < p_val + tolerance):
                    valid = False
                    errors.append(
                        f"Computed p={lib_p:.5g} is not < reported p={p_val_str} (±{tolerance})"
                    )
            elif p_op == '>':
                # Verify library p is strictly greater than reported p (with some tolerance)
                if not (lib_p > p_val - tolerance):
                    valid = False
                    errors.append(
                        f"Computed p={lib_p:.5g} is not > reported p={p_val_str} (±{tolerance})"
                    )
            else:
                valid = False
                errors.append(f"Unsupported p-value operator: {p_op}")
        
        # Print results for the F-test
        print(f"F-Test: F({df1_str}, {df2_str}) = {f_val_str}, p {p_op} {p_val_str}")
        print(f"Status: {'Valid' if valid else 'Invalid'}")
        if errors:
            print(f"  Errors: {', '.join(errors)}")
        print()

    # Validate t-tests
    for match in t_pattern.findall(md_content):
        df_str, t_val_str, p_op, p_val_str = match
        valid = True
        errors = []
        
        # Validate degrees of freedom
        if not df_str.isdigit() or int(df_str) <= 0:
            valid = False
            errors.append(f"Invalid DF: {df_str}")
        
        # Convert DF string to integer
        df = int(df_str) if df_str.isdigit() else None

        # Validate t-value
        t_val = parse_number(t_val_str)
        if t_val is None:
            valid = False
            errors.append(f"Invalid t-value: {t_val_str}")
        
        # Validate p-value components
        p_val = parse_number(p_val_str) if p_val_str else None
        if not p_op or not p_val_str:
            valid = False
            errors.append("Missing p-value operator or value")
        elif p_val is None or not (0 <= p_val <= 1):
            valid = False
            errors.append(f"Invalid p-value: {p_val_str}")

        # If all structural checks pass, attempt to verify the p-value with library
        if valid and (t_val is not None) and (df is not None):
            # Two-sided p-value for t-tests
            # We take the absolute value of t, compute the upper tail, and double it
            # to get the two-sided p-value
            lib_p = 2.0 * (1.0 - t_dist.cdf(abs(t_val), df))
            
            # Compare with p_val according to p_op
            if p_op == '=':
                # Check they are close within some tolerance
                if not isclose(lib_p, p_val, abs_tol=tolerance):
                    valid = False
                    errors.append(
                        f"Reported p={p_val_str} does not match computed p={lib_p:.5g} (within ±{tolerance})"
                    )
            elif p_op == '<':
                # Verify library p < reported p
                if not (lib_p < p_val + tolerance):
                    valid = False
                    errors.append(
                        f"Computed p={lib_p:.5g} is not < reported p={p_val_str} (±{tolerance})"
                    )
            elif p_op == '>':
                # Verify library p > reported p
                if not (lib_p > p_val - tolerance):
                    valid = False
                    errors.append(
                        f"Computed p={lib_p:.5g} is not > reported p={p_val_str} (±{tolerance})"
                    )
            else:
                valid = False
                errors.append(f"Unsupported p-value operator: {p_op}")
        
        # Print results for the t-test
        print(f"t-Test: t({df_str}) = {t_val_str}, p {p_op} {p_val_str}")
        print(f"Status: {'Valid' if valid else 'Invalid'}")
        if errors:
            print(f"  Errors: {', '.join(errors)}")
        print()


# Example usage
if __name__ == "__main__":
    # Adjust path to your test.md as appropriate
    with open('outputs/test/test.md', 'r', encoding='utf-8') as file:
        content = file.read()
    validate_statistics(content)
