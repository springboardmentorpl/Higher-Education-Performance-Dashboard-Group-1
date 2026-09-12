import pandas as pd
import numpy as np
from pathlib import Path

# Get project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

print("=" * 55)
print("STARTING MODULE 3: EDUCATION KPI ENGINEERING")
print("=" * 55)

# Load cleaned dataset
df = pd.read_csv(
    DATA_DIR / "university_cleaned.csv"
)

print("Loaded 'university_cleaned.csv' successfully.")
print(f"Total Institutions to Process: {len(df)}")


# -------------------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------------------

def get_col(df, names, default=0):
    for name in names:
        if name in df.columns:
            return df[name]
    return default


# KPI 1: Global Ranking Score
qs_overall = get_col(df, ["scores_overall_QS"])
the_overall = get_col(df, ["scores_overall_THE"])

df["KPI_Global_Ranking_Score"] = (
    qs_overall + the_overall
) / 2.0


# KPI 2: Research Impact Score
citations_qs = get_col(
    df,
    ["Citations per Faculty Score"]
)

citations_the = get_col(
    df,
    ["scores_citations"]
)

df["KPI_Research_Impact_Score"] = (
    citations_qs + citations_the
) / 2.0


# KPI 3: Faculty-to-Student Ratio
df["KPI_Faculty_To_Student_Ratio"] = get_col(
    df,
    ["stats_student_staff_ratio"]
)


# KPI 4: International Student Percentage
df["KPI_International_Student_Pct"] = get_col(
    df,
    ["stats_pc_intl_students"]
)


# KPI 5: Academic Reputation Score
acad_qs = get_col(
    df,
    ["Academic Reputation Score"]
)

acad_the = get_col(
    df,
    ["scores_teaching"]
)

df["KPI_Academic_Reputation_Score"] = (
    acad_qs + acad_the
) / 2.0


# KPI 6: Research Productivity Index
res_the = get_col(
    df,
    ["scores_research"]
)

net_qs = get_col(
    df,
    ["International Research Network Score"]
)

df["KPI_Research_Productivity_Index"] = (
    res_the * 0.6
) + (
    net_qs * 0.4
)


# -------------------------------------------------------------
# EXPORT
# -------------------------------------------------------------

df.to_csv(
    DATA_DIR / "university_final_dataset.csv",
    index=False
)

print(
    "\nCSV saved: "
    "'university_final_dataset.csv'"
)


# Optional Excel export
try:
    with pd.ExcelWriter(
        DATA_DIR / "university_final_dataset.xlsx",
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="University_KPIs",
            index=False
        )

    print(
        "Excel saved: "
        "'university_final_dataset.xlsx'"
    )

except Exception as e:
    print(f"Excel export skipped: {e}")


# -------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------

print("\n" + "=" * 55)
print("MODULE 3 KPI SUMMARY")
print("=" * 55)

kpi_cols = [
    "KPI_Global_Ranking_Score",
    "KPI_Research_Impact_Score",
    "KPI_Faculty_To_Student_Ratio",
    "KPI_International_Student_Pct",
    "KPI_Academic_Reputation_Score",
    "KPI_Research_Productivity_Index"
]

summary = (
    df[kpi_cols]
    .describe()
    .round(2)
    .T[
        ["mean", "std", "min", "50%", "max"]
    ]
)

summary.columns = [
    "Mean",
    "Std Dev",
    "Min",
    "Median",
    "Max"
]

print(summary)

print("\nModule 3 KPI Engineering successfully completed!")