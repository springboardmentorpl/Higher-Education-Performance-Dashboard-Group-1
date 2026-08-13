import pandas as pd
import re
from pathlib import Path


# ============================================================
# EDUVISION - MODULE 1
# UNIVERSITY DATA COLLECTION & DATASET INTEGRATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "merged"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

QS_FILE = RAW_DIR / "2026 QS World University Rankings.csv"
OLD_FILE = RAW_DIR / "university_rankings.csv"


def normalize_name(value):
    """Standardize university names for matching."""

    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    value = value.replace("&", "and")

    # Remove common punctuation
    value = re.sub(r"[^\w\s]", " ", value)

    # Normalize spaces
    value = re.sub(r"\s+", " ", value).strip()

    return value


def normalize_country(value):
    """Standardize country names."""

    if pd.isna(value):
        return ""

    value = str(value).strip()

    replacements = {
        "United States of America": "United States",
        "USA": "United States",
        "US": "United States",
        "UK": "United Kingdom",
        "Russian Federation": "Russia",
        "South Korea": "South Korea",
        "Korea, Republic of": "South Korea",
        "Hong Kong SAR": "Hong Kong",
        "Türkiye": "Turkey",
        "Czechia": "Czech Republic",
    }

    return replacements.get(value, value)


print("=" * 60)
print("EDUVISION - UNIVERSITY DATA COLLECTION")
print("=" * 60)


# ============================================================
# 1. LOAD DATASETS
# ============================================================

print("\nLoading datasets...")

qs = pd.read_csv(QS_FILE)
old = pd.read_csv(OLD_FILE)

print(f"2026 QS dataset: {qs.shape}")
print(f"Historical dataset: {old.shape}")


# ============================================================
# 2. STANDARDIZE COLUMN NAMES
# ============================================================

qs = qs.rename(columns={
    "2026 Rank": "Rank_2026",
    "Previous Rank": "Previous_Rank_2025",
    "Institution Name": "Institution_Name",
    "Country/Territory": "Country",
    "Region": "Region",
    "Size": "Size",
    "Focus": "Focus",
    "Research": "Research",
    "Status": "Status",

    "AR SCORE": "Academic_Reputation_Score_2026",
    "AR RANK": "Academic_Reputation_Rank_2026",

    "ER SCORE": "Employer_Reputation_Score_2026",
    "ER RANK": "Employer_Reputation_Rank_2026",

    "FSR SCORE": "Faculty_Student_Score_2026",
    "FSR RANK": "Faculty_Student_Rank_2026",

    "CPF SCORE": "Citations_per_Faculty_Score_2026",
    "CPF RANK": "Citations_per_Faculty_Rank_2026",

    "IFR SCORE": "International_Faculty_Score_2026",
    "IFR RANK": "International_Faculty_Rank_2026",

    "ISR SCORE": "International_Students_Score_2026",
    "ISR RANK": "International_Students_Rank_2026",

    "ISD SCORE": "International_Students_Diversity_Score_2026",
    "ISD RANK": "International_Students_Diversity_Rank_2026",

    "IRN SCORE": "International_Research_Network_Score_2026",
    "IRN RANK": "International_Research_Network_Rank_2026",

    "EO SCORE": "Employment_Outcomes_Score_2026",
    "EO RANK": "Employment_Outcomes_Rank_2026",

    "SUS SCORE": "Sustainability_Score_2026",
    "SUS RANK": "Sustainability_Rank_2026",

    "Overall SCORE": "Overall_Score_2026"
})


old = old.rename(columns={
    "2024 RANK": "Rank_2024",
    "2023 RANK": "Rank_2023",
    "Institution Name": "Institution_Name",
    "Country Code": "Country_Code",
    "Country": "Country",
    "SIZE": "Size",
    "FOCUS": "Focus",
    "RES.": "Research",
    "AGE": "Age",
    "STATUS": "Status",

    "Academic Reputation Score": "Academic_Reputation_Score_2024",
    "Academic Reputation Rank": "Academic_Reputation_Rank_2024",

    "Employer Reputation Score": "Employer_Reputation_Score_2024",
    "Employer Reputation Rank": "Employer_Reputation_Rank_2024",

    "Faculty Student Score": "Faculty_Student_Score_2024",
    "Faculty Student Rank": "Faculty_Student_Rank_2024",

    "Citations per Faculty Score": "Citations_per_Faculty_Score_2024",
    "Citations per Faculty Rank": "Citations_per_Faculty_Rank_2024",

    "International Faculty Score": "International_Faculty_Score_2024",
    "International Faculty Rank": "International_Faculty_Rank_2024",

    "International Students Score": "International_Students_Score_2024",
    "International Students Rank": "International_Students_Rank_2024",

    "International Research Network Score": "International_Research_Network_Score_2024",
    "International Research Network Rank": "International_Research_Network_Rank_2024",

    "Employment Outcomes Score": "Employment_Outcomes_Score_2024",
    "Employment Outcomes Rank": "Employment_Outcomes_Rank_2024",

    "Sustainability Score": "Sustainability_Score_2024",
    "Sustainability Rank": "Sustainability_Rank_2024",

    "Overall SCORE": "Overall_Score_2024"
})


# ============================================================
# 3. STANDARDIZE UNIVERSITY NAMES AND COUNTRIES
# ============================================================

qs["Match_Name"] = qs["Institution_Name"].apply(normalize_name)
old["Match_Name"] = old["Institution_Name"].apply(normalize_name)

qs["Country"] = qs["Country"].apply(normalize_country)
old["Country"] = old["Country"].apply(normalize_country)


# ============================================================
# 4. REMOVE DUPLICATES
# ============================================================

qs = qs.drop_duplicates(
    subset=["Match_Name", "Country"],
    keep="first"
)

old = old.drop_duplicates(
    subset=["Match_Name", "Country"],
    keep="first"
)


print("\nAfter duplicate removal:")
print(f"2026 QS: {qs.shape}")
print(f"Historical: {old.shape}")


# ============================================================
# 5. MERGE DATASETS
# ============================================================

print("\nMerging datasets...")

merged = pd.merge(
    qs,
    old,
    on=["Match_Name", "Country"],
    how="outer",
    suffixes=("_QS", "_Historical")
)


# ============================================================
# 6. COMBINE COMMON DESCRIPTIVE FIELDS
# ============================================================

for column in [
    "Institution_Name",
    "Region",
    "Size",
    "Focus",
    "Research",
    "Status"
]:

    qs_col = f"{column}_QS"
    hist_col = f"{column}_Historical"

    if qs_col in merged.columns and hist_col in merged.columns:

        merged[column] = (
            merged[qs_col]
            .combine_first(merged[hist_col])
        )

        merged.drop(
            columns=[qs_col, hist_col],
            inplace=True
        )


# ============================================================
# 7. REMOVE MATCHING HELPER COLUMN
# ============================================================

merged.drop(
    columns=["Match_Name"],
    inplace=True,
    errors="ignore"
)


# ============================================================
# 8. REORDER IMPORTANT COLUMNS
# ============================================================

priority_columns = [
    "Institution_Name",
    "Country",
    "Country_Code",
    "Region",
    "Size",
    "Focus",
    "Research",
    "Age",
    "Status",

    "Rank_2026",
    "Previous_Rank_2025",
    "Rank_2024",
    "Rank_2023",

    "Overall_Score_2026",
    "Overall_Score_2024"
]

existing_priority = [
    col for col in priority_columns
    if col in merged.columns
]

remaining_columns = [
    col for col in merged.columns
    if col not in existing_priority
]

merged = merged[
    existing_priority + remaining_columns
]


# ============================================================
# 9. SAVE MERGED DATASET
# ============================================================

csv_output = OUTPUT_DIR / "university_merged_data.csv"
excel_output = OUTPUT_DIR / "university_merged_data.xlsx"

merged.to_csv(
    csv_output,
    index=False
)

merged.to_excel(
    excel_output,
    index=False
)


# ============================================================
# 10. REPORT
# ============================================================

print("\n" + "=" * 60)
print("DATASET INTEGRATION COMPLETE")
print("=" * 60)

print(f"\nMerged shape: {merged.shape}")

print(f"\nCSV saved to:")
print(csv_output)

print(f"\nExcel saved to:")
print(excel_output)

print("\nDuplicate rows:", merged.duplicated().sum())

print("\nUniversity count:", len(merged))

print("\nDataset integration completed successfully.")