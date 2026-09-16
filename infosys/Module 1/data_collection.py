import pandas as pd

# Module 1: Data Collection
# Load the raw university ranking dataset and export it as a CSV file.

SOURCE_FILE = "university_raw_data.csv.xlsx"
OUTPUT_FILE = "university_raw_data.csv"

# Read the raw dataset
df = pd.read_excel(SOURCE_FILE)

# Save the collected/raw data without modifying the records
df.to_csv(OUTPUT_FILE, index=False)

print(f"Data collection completed successfully.")
print(f"Rows collected: {len(df)}")
print(f"Columns collected: {len(df.columns)}")
print(f"Raw dataset saved as: {OUTPUT_FILE}")
