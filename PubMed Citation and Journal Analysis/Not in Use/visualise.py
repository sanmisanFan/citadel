import pandas as pd

# Read the data
file_path = './journal_matrix.csv'  # Update this with the actual path to your CSV file

# Assuming the file is a CSV, you can read it using pandas
# Adjust the delimiter as necessary, the image suggests it's comma-separated
data = pd.read_csv(file_path, header=None)

# Set the first column as index if it represents the journal names
data.set_index(0, inplace=True)

# Convert all values to numeric, setting errors='coerce' will convert non-numeric values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Optionally fill NaNs with 0s or another value if needed
data = data.fillna(0)

# List all journal pairs with their citation counts
pairs = []

for citing_journal in data.index:
    for cited_journal in data.columns:
        count = data.loc[citing_journal, cited_journal]
        pairs.append((citing_journal, cited_journal, count))

# Display the results
pairs_df = pd.DataFrame(pairs, columns=['Citing Journal', 'Cited Journal', 'Count'])
print(pairs_df)

# Optionally, save to a CSV file
pairs_df.to_csv('all_citation_pairs.csv', index=False)
