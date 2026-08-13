import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "university_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data" / "cleaned"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUTPUT = OUTPUT_DIR / "university_cleaned.csv"
EXCEL_OUTPUT = OUTPUT_DIR / "university_cleaned.xlsx"

CORE_COLUMNS = [
    "Global_Ranking_Score",
    "Academic_Reputation_Score",
    "Employer_Reputation_Score",
    "Faculty_Student_Score",
    "Citations_per_Faculty_Score",
    "International_Faculty_Score",
    "International_Students_Score",
    "International_Research_Network_Score",
    "Employment_Outcomes_Score",
    "Sustainability_Score",
]

print("=" * 65)
print("EDUVISION - FINAL MODULE 2 CLEANED DATASET")
print("=" * 65)

df = pd.read_csv(INPUT_FILE)

print("\nOriginal cleaned dataset:")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Keep only records having all required core indicators
final_df = df.dropna(subset=CORE_COLUMNS).copy()

# Remove any remaining duplicate university-country combinations
final_df = final_df.drop_duplicates(
    subset=["Institution_Name", "Country"],
    keep="first"
)

# Sort by current ranking
if "Current_Rank" in final_df.columns:
    final_df = final_df.sort_values(
        by="Current_Rank",
        na_position="last"
    )

# Reset index
final_df = final_df.reset_index(drop=True)

# Save CSV
final_df.to_csv(
    CSV_OUTPUT,
    index=False
)

# Save Excel
final_df.to_excel(
    EXCEL_OUTPUT,
    index=False,
    sheet_name="University Data"
)

# Verification
missing_core = final_df[CORE_COLUMNS].isna().sum().sum()
duplicate_rows = final_df.duplicated().sum()

total_core_cells = len(final_df) * len(CORE_COLUMNS)

missing_percentage = (
    missing_core / total_core_cells * 100
    if total_core_cells > 0
    else 0
)

print("\n" + "=" * 65)
print("FINAL DATASET VERIFICATION")
print("=" * 65)

print("\nFinal rows:", len(final_df))
print("Final columns:", len(final_df.columns))
print("Core indicators:", len(CORE_COLUMNS))
print("Missing core cells:", missing_core)
print("Core missing percentage:", round(missing_percentage, 2), "%")
print("Duplicate rows:", duplicate_rows)

print("\nCore indicator completeness:")

for column in CORE_COLUMNS:
    valid = final_df[column].notna().sum()
    percentage = valid / len(final_df) * 100

    print(
        f"{column:<45}"
        f"{valid:>5} / {len(final_df)} "
        f"({percentage:.2f}%)"
    )

print("\nCSV created:")
print(CSV_OUTPUT)

print("\nExcel created:")
print(EXCEL_OUTPUT)

print("\n" + "=" * 65)

if (
    len(final_df) == 851
    and missing_core == 0
    and duplicate_rows == 0
):
    print("STATUS: MODULE 2 COMPLETE")
    print("851 complete records successfully created.")
else:
    print("STATUS: CHECK REQUIRED")

print("=" * 65)