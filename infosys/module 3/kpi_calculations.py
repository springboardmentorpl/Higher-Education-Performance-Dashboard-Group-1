"""
KPI Calculations - Global Score, Academic Reputation Score,
Faculty-to-Student Ratio Score

Run this AFTER your main university_rankings_analysis.py script,
or paste this code as new cells at the end of your notebook.
It reads the final cleaned dataset, adds three KPI columns, and
saves the result back to Excel so the KPIs are reflected there.
"""

import pandas as pd

# Load your cleaned dataset (the one already produced by the main script)
df = pd.read_csv("final_cleaned_university_dataset.csv")

# ------------------------------------------------------------------
# KPI 1: Academic Reputation Score
# Directly from QS's own Academic Reputation subscore (already 0-100 scaled)
# ------------------------------------------------------------------
df["academic_reputation_score"] = df["qs_academic_reputation"]

# ------------------------------------------------------------------
# KPI 2: Faculty-to-Student Ratio Score
# Directly from QS's own Faculty/Student subscore (already 0-100 scaled)
# ------------------------------------------------------------------
df["faculty_student_ratio_score"] = df["qs_faculty_student"]

# ------------------------------------------------------------------
# KPI 3: Global Score
# A weighted combination of QS's individual indicator scores, following
# QS's published methodology weights. Adjust these weights if Ankita
# specified different percentages.
# ------------------------------------------------------------------
weights = {
    "qs_academic_reputation": 0.30,
    "qs_employer_reputation": 0.15,
    "qs_faculty_student": 0.10,
    "qs_citations_per_faculty": 0.20,
    "qs_international_faculty": 0.05,
    "qs_international_students": 0.05,
    "qs_international_research_network": 0.05,
    "qs_employment_outcomes": 0.05,
    "qs_sustainability": 0.05,
}

df["global_score"] = sum(
    df[col].fillna(0) * weight for col, weight in weights.items()
)
df["global_score"] = df["global_score"].round(2)

# ------------------------------------------------------------------
# Preview
# ------------------------------------------------------------------
print(df[[
    "university_name",
    "academic_reputation_score",
    "faculty_student_ratio_score",
    "global_score"
]].head(10))

# ------------------------------------------------------------------
# Save back to Excel so the KPIs are reflected there
# ------------------------------------------------------------------
df.to_excel("final_cleaned_university_dataset.xlsx", index=False, engine="openpyxl")
df.to_csv("final_cleaned_university_dataset.csv", index=False)

print("\nKPI columns added and saved to:")
print(" - final_cleaned_university_dataset.xlsx")
print(" - final_cleaned_university_dataset.csv")
