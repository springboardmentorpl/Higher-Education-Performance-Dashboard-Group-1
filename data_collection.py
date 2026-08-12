import pandas as pd

# Load datasets
df1 = pd.read_csv(
    "QS World University Rankings 2025 (Top global universities).csv",
    encoding="latin-1"
)

df2 = pd.read_csv(
    "CleanData_universityRanking.csv"
)

# Rename university column for consistency
df1 = df1.rename(columns={"Institution_Name": "University"})

# Standardize text for matching
df1["University"] = df1["University"].astype(str).str.strip()
df1["Location"] = df1["Location"].astype(str).str.strip()

df2["University"] = df2["University"].astype(str).str.strip()
df2["Location"] = df2["Location"].astype(str).str.strip()

# Remove duplicate university-location combinations
df2 = df2.drop_duplicates(
    subset=["University", "Location"]
)

# LEFT MERGE
merged_data = pd.merge(
    df1,
    df2,
    on=["University", "Location"],
    how="left",
    suffixes=("", "_dataset2")
)

# Save raw merged dataset
merged_data.to_csv(
    "university_raw_data.csv",
    index=False
)

print("Module 1 completed successfully!")
print("Shape:", merged_data.shape)
