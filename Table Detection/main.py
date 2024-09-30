import tabula

import pandas as pd
from scipy import stats

# Extract tables from the PDF
tables = tabula.read_pdf("../known_pdfs/srep45125.pdf", pages='all', multiple_tables=True)

# Save tables to CSV
for i, table in enumerate(tables):
    table.to_csv(f'table_{i}.csv', index=False)

# Print the extracted tables
for table in tables:
    print(table)




# Load the CSV file
df = pd.read_csv('table_2.csv')

# Function to clean and extract only the numerical value (mean) from the data
def extract_mean(value):
    return float(value.split('+')[0].strip())

# Extract values for GnRH-1 for both males and females across the tissues
gnrh_1_values = df[df['Gene'] == 'GnRH-I']

# Get the male and female values for Hypothalamus, Pituitary, and Gonads
male_values = [
    extract_mean(gnrh_1_values['Unnamed: 1'].values[0]),  # Hypothalamus Male
    extract_mean(gnrh_1_values['Unnamed: 0'].values[0]),  # Pituitary Male
    extract_mean(gnrh_1_values['Unnamed: 2'].values[0])   # Gonads Male
]

female_values = [
    extract_mean(gnrh_1_values['Hypothalamus'].values[0]),  # Hypothalamus Female
    extract_mean(gnrh_1_values['Pituitary'].values[0]),     # Pituitary Female
    extract_mean(gnrh_1_values['Gonads'].values[0])         # Gonads Female
]

# Perform t-test
t_stat, p_value = stats.ttest_ind(male_values, female_values)
print(f"T-statistic: {t_stat}, P-value: {p_value}")
