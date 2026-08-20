import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# EDUVISION - EDUCATION KPI ENGINEERING
# Module 3 - Milestone 2
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "university_cleaned.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "final"
OUTPUT_FILE = OUTPUT_DIR / "university_final_dataset.xlsx"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("EDUVISION - EDUCATION KPI ENGINEERING")
print("=" * 65)

# ------------------------------------------------------------
# 1. LOAD CLEANED DATASET
# ------------------------------------------------------------

print("\nLoading cleaned dataset...")

df = pd.read_excel(INPUT_FILE)

print(f"Input rows: {len(df)}")
print(f"Input columns: {len(df.columns)}")

# ------------------------------------------------------------
# 2. REQUIRED SOURCE COLUMNS
# ------------------------------------------------------------

required_columns = [
    "Global_Ranking_Score",
    "Academic_Reputation_Score",
    "Faculty_Student_Score",
    "International_Students_Score",
    "Citations_per_Faculty_Score",
    "International_Research_Network_Score"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# Convert KPI source fields to numeric
for col in required_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ------------------------------------------------------------
# 3. GLOBAL RANKING SCORE
# ------------------------------------------------------------

# The cleaned dataset already contains the normalized
# Global Ranking Score from the QS ranking data.

df["KPI_Global_Ranking_Score"] = (
    df["Global_Ranking_Score"]
)

# ------------------------------------------------------------
# 4. RESEARCH IMPACT SCORE
# ------------------------------------------------------------

# Research impact is represented using two research-related
# indicators available in the cleaned dataset:
#
# - Citations per Faculty Score
# - International Research Network Score
#
# Equal-weight average is used.

df["KPI_Research_Impact_Score"] = (
    df[
        [
            "Citations_per_Faculty_Score",
            "International_Research_Network_Score"
        ]
    ].mean(axis=1)
)

# ------------------------------------------------------------
# 5. FACULTY-TO-STUDENT RATIO
# ------------------------------------------------------------

# The source dataset does not contain raw faculty counts or
# raw student counts. Therefore an actual numerical
# faculty/student ratio cannot be calculated from this dataset.
#
# The available Faculty Student Score is retained as the
# score-based KPI representation.

df["KPI_Faculty_to_Student_Ratio"] = (
    df["Faculty_Student_Score"]
)

# ------------------------------------------------------------
# 6. INTERNATIONAL STUDENT PERCENTAGE
# ------------------------------------------------------------

# The source dataset contains International Students Score,
# but does not contain raw international-student and total-
# student counts.
#
# Therefore the available International Students Score is
# retained as the score-based representation.

df["KPI_International_Student_Percentage"] = (
    df["International_Students_Score"]
)

# ------------------------------------------------------------
# 7. ACADEMIC REPUTATION SCORE
# ------------------------------------------------------------

# Academic Reputation Score is already available as a
# normalized ranking indicator.

df["KPI_Academic_Reputation_Score"] = (
    df["Academic_Reputation_Score"]
)

# ------------------------------------------------------------
# 8. RESEARCH PRODUCTIVITY INDEX
# ------------------------------------------------------------

# Research Productivity Index is calculated from the two
# research-related quantitative indicators available:
#
# - Citations per Faculty Score
# - International Research Network Score
#
# Equal-weight average is used.

df["KPI_Research_Productivity_Index"] = (
    df[
        [
            "Citations_per_Faculty_Score",
            "International_Research_Network_Score"
        ]
    ].mean(axis=1)
)

# ------------------------------------------------------------
# 9. ROUND KPI VALUES
# ------------------------------------------------------------

kpi_columns = [
    "KPI_Global_Ranking_Score",
    "KPI_Research_Impact_Score",
    "KPI_Faculty_to_Student_Ratio",
    "KPI_International_Student_Percentage",
    "KPI_Academic_Reputation_Score",
    "KPI_Research_Productivity_Index"
]

for col in kpi_columns:
    df[col] = df[col].round(2)

# ------------------------------------------------------------
# 10. KPI SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("KPI CALCULATION SUMMARY")
print("=" * 65)

for col in kpi_columns:
    valid = df[col].notna().sum()
    missing = df[col].isna().sum()

    print(
        f"{col:<45} "
        f"{valid} valid | {missing} missing"
    )

# ------------------------------------------------------------
# 11. FINAL DATASET VERIFICATION
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("FINAL DATASET VERIFICATION")
print("=" * 65)

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print(
    f"Duplicate rows: {df.duplicated().sum()}"
)

print(
    f"KPI columns added: {len(kpi_columns)}"
)

print("\nSix KPIs:")

for col in kpi_columns:
    print(f" - {col}")

# ------------------------------------------------------------
# 12. SAVE FINAL EXCEL DATASET
# ------------------------------------------------------------

df.to_excel(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 65)
print("MODULE 3 KPI ENGINEERING COMPLETE")
print("=" * 65)

print(f"\nExcel created:")
print(OUTPUT_FILE)

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nStatus: SUCCESS")
print("=" * 65)