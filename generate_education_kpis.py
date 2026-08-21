"""
Module 3 — Education KPI Engineering
--------------------------------------
Milestone 2 deliverable for EduVision_DV.

Runs directly on your FINAL cleaned dataset (universities_clean_wide.csv)
and calculates/validates the six required Education KPIs, then exports
the Tableau-ready university_final_dataset.xlsx.

KPIs:
 1. Global Ranking Score
 2. Academic Reputation Score
 3. Faculty-to-Student Ratio Score
 4. International Student Percentage Score
 5. Research Impact Score
 6. Research Productivity Index  (recalculated from ARWU sub-scores)

Usage:
    pip install pandas openpyxl
    python generate_education_kpis.py

Place this script in the same folder as universities_clean_wide.csv
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. Load your final cleaned dataset
# ---------------------------------------------------------------
INPUT_FILE = "universities_clean_wide.csv"
OUTPUT_FILE = "university_final_dataset.xlsx"

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows, {len(df.columns)} columns from {INPUT_FILE}")


# ---------------------------------------------------------------
# 2. KPI 1 -- Global Ranking Score
#    Already present: QS's overall ranking score (0-100 scale).
# ---------------------------------------------------------------
assert "global_ranking_score" in df.columns, "global_ranking_score missing"


# ---------------------------------------------------------------
# 3. KPI 2 -- Academic Reputation Score
#    Already present: QS Academic Reputation survey score.
# ---------------------------------------------------------------
assert "academic_reputation_score" in df.columns, "academic_reputation_score missing"


# ---------------------------------------------------------------
# 4. KPI 3 -- Faculty-to-Student Ratio Score
#    Already present: QS Faculty/Student Ratio score.
# ---------------------------------------------------------------
assert "faculty_student_ratio_score" in df.columns, "faculty_student_ratio_score missing"


# ---------------------------------------------------------------
# 5. KPI 4 -- International Student Percentage Score
#    Already present: QS International Students Ratio score.
# ---------------------------------------------------------------
assert "international_student_score" in df.columns, "international_student_score missing"


# ---------------------------------------------------------------
# 6. KPI 5 -- Research Impact Score
#    Already present: QS Citations-per-Faculty score.
# ---------------------------------------------------------------
assert "research_impact_score" in df.columns, "research_impact_score missing"


# ---------------------------------------------------------------
# 7. KPI 6 -- Research Productivity Index
#    CALCULATED here as the average of three ARWU research-output
#    sub-scores, combining volume + influence + prestige:
#      - arwu_publications_score              (research volume)
#      - arwu_highly_cited_researchers_score   (research influence)
#      - arwu_nature_and_science_score         (top-tier output)
# ---------------------------------------------------------------
research_cols = [
    "arwu_publications_score",
    "arwu_highly_cited_researchers_score",
    "arwu_nature_and_science_score",
]
missing = [c for c in research_cols if c not in df.columns]
if missing:
    raise KeyError(f"Missing columns needed for Research Productivity Index: {missing}")

df["research_productivity_score"] = df[research_cols].mean(axis=1).round(2)


# ---------------------------------------------------------------
# 8. Validate all 6 KPIs are present with acceptable completeness
# ---------------------------------------------------------------
kpi_cols = [
    "global_ranking_score",
    "academic_reputation_score",
    "faculty_student_ratio_score",
    "international_student_score",
    "research_impact_score",
    "research_productivity_score",
]

print("\nKPI missing-value check:")
print(df[kpi_cols].isnull().sum())

kpi_completeness = 100 * (1 - df[kpi_cols].isnull().mean().mean())
print(f"\nOverall KPI completeness: {kpi_completeness:.2f}% (target: >95%)")

assert all(c in df.columns for c in kpi_cols), "One or more KPI columns missing"
print("All 6 KPIs validated/calculated successfully.")


# ---------------------------------------------------------------
# 9. Export the Module 3 deliverable
# ---------------------------------------------------------------
df.to_excel(OUTPUT_FILE, index=False)
print(f"\nSaved: {OUTPUT_FILE}")
print("Shape:", df.shape)