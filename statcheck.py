from scipy import stats
import re
import flor


# Function to round the computed p-value to the same number of decimals as the reported p-value
def round_to_reported(computed_p, reported_p):
    decimal_places = len(str(reported_p).split(".")[1])
    return round(computed_p, decimal_places)


# Extract F-tests, t-tests, and Chi-square tests using regex
f_test_pattern = r"[fF]\s*[\(\[]\s*(\d+),\s*(\d+)\s*[\)\]]\s*=\s*([\d.]+)[,;]\s*[pP]\s*(<|>|=)\s*(\d*(?:\.\d+)?)"
t_test_pattern = r"[tT]\s*[\(\[]\s*(\d+)\s*[\)\]]\s*=\s*([\d.]+)\s*[;,]?\s*[pP]\s*=\s*(\d*(?:\.\d+)?)"
chi_square_test_pattern = r"[Xx]\s*(?:²|\^2|2)?\s*[\(\[]\s*(\d+)\s*(?:,[Nn]\s*=\s*\d+)?\s*[\)\]]\s*=\s*([\d.]+)[,;]\s*[pP]\s*(<|>|=)\s*(\d*(?:\.\d+)?)"


def find_tests(text, pattern):
    return re.findall(pattern, text)


def check_f_test(dfn, dfd, f_statistic, inequality, reported_p):
    computed_p = stats.f.sf(f_statistic, dfn, dfd)
    reported_p = float(reported_p)
    rounded_computed_p = round_to_reported(computed_p, reported_p)

    if inequality == "=" and rounded_computed_p == reported_p:
        return (
            f"Valid F-test: F({dfn}, {dfd}) = {f_statistic}, p = {rounded_computed_p}"
        )
    elif inequality == "<" and computed_p < reported_p:
        return f"Valid F-test: F({dfn}, {dfd}) = {f_statistic}, p < {reported_p}"
    elif inequality == ">" and computed_p > reported_p:
        return f"Valid F-test: F({dfn}, {dfd}) = {f_statistic}, p > {reported_p}"
    else:
        return f"Invalid F-test: F({dfn}, {dfd}) = {f_statistic}, p {inequality} {reported_p} (Computed p = {rounded_computed_p})"


def check_chi_square_test(dof, chi_statistic, inequality, reported_p):
    computed_p = stats.chi2.sf(chi_statistic, dof)
    reported_p = float(reported_p)
    rounded_computed_p = round_to_reported(computed_p, reported_p)
    if inequality == "=" and rounded_computed_p == reported_p:
        return f"Valid Chi-square test: χ²({dof}) = {chi_statistic}, p = {rounded_computed_p}"
    elif inequality == "<" and computed_p < reported_p:
        return f"Valid Chi-square test: χ²({dof}) = {chi_statistic}, p < {reported_p}"
    elif inequality == ">" and computed_p > reported_p:
        return f"Valid Chi-square test: χ²({dof}) = {chi_statistic}, p > {reported_p}"
    else:
        return f"Invalid Chi-square test: χ²({dof}) = {chi_statistic}, p {inequality} {reported_p} (Computed p = {rounded_computed_p})"


def check_t_test(df, t_statistic, reported_p):
    computed_p = stats.t.sf(abs(t_statistic), df) * 2  # two-tailed
    rounded_computed_p = round_to_reported(computed_p, reported_p)
    if rounded_computed_p == reported_p:
        return f"Valid t-test: t({df}) = {t_statistic}, p = {reported_p}"
    else:
        return f"Invalid t-test: t({df}) = {t_statistic}, p = {reported_p} (Computed p = {rounded_computed_p})"


# Main function to process the PDF file and check tests
def process_pdf_file(page_text):
    text = " ".join(page_text["page_text"].values)
    f_tests = find_tests(text, f_test_pattern)
    t_tests = find_tests(text, t_test_pattern)
    chi_tests = find_tests(text, chi_square_test_pattern)

    for test in f_tests:
        dfn, dfd, f_statistic, inequality, reported_p = test
        dfn, dfd, f_statistic = int(dfn), int(dfd), float(f_statistic)
        print(check_f_test(dfn, dfd, f_statistic, inequality, reported_p))

    for test in chi_tests:
        dof, chi_statistic, inequality, reported_p = test
        dof, chi_statistic = int(dof), float(chi_statistic)
        print(check_chi_square_test(dof, chi_statistic, inequality, reported_p))

    for test in t_tests:
        df, t_statistic, reported_p = test
        df = int(df)
        t_statistic, reported_p = float(t_statistic), float(reported_p)
        print(check_t_test(df, t_statistic, reported_p))


if __name__ == "__main__":
    page_text = flor.dataframe("page_text")
    known_pdfs = page_text["pdf_value"].drop_duplicates().values
    for pdf_path in flor.loop("pdf", known_pdfs):
        print()
        print(f"Checking Statistics on {pdf_path}")
        process_pdf_file(page_text[page_text["pdf_value"] == pdf_path])
