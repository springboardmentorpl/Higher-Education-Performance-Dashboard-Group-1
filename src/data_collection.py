import pandas as pd
from pathlib import Path

# Get project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

print("Loading datasets...")

# Load QS dataset
qs_df = pd.read_csv(
    DATA_DIR / "qs_rankings_2024.csv",
    encoding="utf-8"
)

# Load THE dataset from Excel
the_df = pd.read_excel(
    DATA_DIR / "world_rankings_cleaned.xlsx"
)

print("QS dataset:", qs_df.shape)
print("THE dataset:", the_df.shape)

print("\nDatasets loaded successfully!")

print("\nQS columns:")
print(qs_df.columns.tolist())

print("\nTHE columns:")
print(the_df.columns.tolist())


# Find universities that appear in both datasets

qs_names = set(
    qs_df["Institution_name"]
    .dropna()
    .astype(str)
    .str.strip()
)

the_names = set(
    the_df["Institution_name"]
    .dropna()
    .astype(str)
    .str.strip()
)

common_universities = qs_names.intersection(the_names)

print("\nNumber of QS universities:", len(qs_names))
print("Number of THE universities:", len(the_names))
print("Universities present in BOTH datasets:", len(common_universities))

print("\nSample common universities:")
print(list(common_universities)[:10])


# Check for common universities after basic name cleaning

qs_names_clean = (
    qs_df["Institution_name"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
)

the_names_clean = (
    the_df["Institution_name"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
)

common_clean = set(qs_names_clean).intersection(set(the_names_clean))

print("\nUniversities in both datasets after name cleaning:", len(common_clean))


# Find columns that exist in both datasets

common_columns = set(qs_df.columns).intersection(set(the_df.columns))

print("\nCommon column names:")
print(sorted(common_columns))


# Rename columns to identify their ranking source

qs_df = qs_df.rename(columns={
    "rank": "QS Rank",
    "location": "QS Location",
    "scores_overall": "QS Overall Score"
})

the_df = the_df.rename(columns={
    "Rank": "THE Rank",
    "location": "THE Location",
    "scores_overall": "THE Overall Score"
})

print("\nColumns renamed successfully!")


# --------------------------------------------------
# APPEND THE TWO DATASETS
# --------------------------------------------------

print("\nAppending QS and THE datasets...")

combined_df = pd.concat(
    [qs_df, the_df],
    ignore_index=True,
    sort=False
)

print("Combined dataset shape:", combined_df.shape)


# Save the combined raw dataset

combined_df.to_csv(
    DATA_DIR / "university_raw_data.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nRaw combined dataset saved successfully!")