import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Load final cleaned dataset
# --------------------------------------------------

df = pd.read_csv("university_tableau_ready.csv")

print("Dataset loaded successfully.")
print("Original shape:", df.shape)


# --------------------------------------------------
# 2. Convert ranking columns to numeric
# --------------------------------------------------

def extract_rank(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # Extract first number from values such as:
    # "1", "101-150", "1001–1200"
    import re

    match = re.search(r"\d+", value)

    if match:
        return float(match.group())

    return np.nan


df["QS_Rank_Numeric"] = df["QS_Rank"].apply(extract_rank)
df["THE_Rank_Numeric"] = df["THE_Rank"].apply(extract_rank)


# --------------------------------------------------
# 3. Global Ranking Score
# --------------------------------------------------
# Lower rank = better.
#
# Normalize QS and THE rankings separately:
#
# Score = 1 - ((Rank - 1) / (Maximum Rank - 1))
#
# Then combine QS and THE equally.
# Final score is on a 0-100 scale.
# --------------------------------------------------

qs_max_rank = df["QS_Rank_Numeric"].max()
the_max_rank = df["THE_Rank_Numeric"].max()

df["QS_Rank_Score"] = (
    1 - (df["QS_Rank_Numeric"] - 1) /
    (qs_max_rank - 1)
) * 100

df["THE_Rank_Score"] = (
    1 - (df["THE_Rank_Numeric"] - 1) /
    (the_max_rank - 1)
) * 100

df["Global_Ranking_Score"] = (
    df["QS_Rank_Score"] +
    df["THE_Rank_Score"]
) / 2


# --------------------------------------------------
# 4. Research Impact Score
# --------------------------------------------------
# Average of THE Research Environment
# and THE Research Quality.
# --------------------------------------------------

df["Research_Impact_Score"] = df[
    [
        "THE_Research_Environment",
        "THE_Research_Quality"
    ]
].mean(axis=1)


# --------------------------------------------------
# 5. Faculty-to-Student Ratio
# --------------------------------------------------
# The original column represents students per faculty.
#
# Faculty-to-student ratio = 1 / Student-Faculty Ratio
# --------------------------------------------------

df["Faculty_to_Student_Ratio"] = (
    1 / df["Student_Faculty_Ratio"]
)


# --------------------------------------------------
# 6. Estimate total students
# --------------------------------------------------
# Student-Faculty Ratio represents students per faculty.
#
# Estimated students =
# Faculty Count × Student-Faculty Ratio
# --------------------------------------------------

df["Estimated_Total_Students"] = (
    df["Faculty_Count"] *
    df["Student_Faculty_Ratio"]
)


# --------------------------------------------------
# 7. International Student Percentage
# --------------------------------------------------

df["International_Student_Percentage"] = (
    df["International_Students"] /
    df["Estimated_Total_Students"]
) * 100

# Remove mathematically invalid percentages
df.loc[
    (df["International_Student_Percentage"] < 0) |
    (df["International_Student_Percentage"] > 100),
    "International_Student_Percentage"
] = np.nan


# --------------------------------------------------
# 8. Academic Reputation Score
# --------------------------------------------------
# No direct Academic Reputation column exists
# in the available dataset.
#
# Therefore THE Teaching score is used as a
# teaching-based academic reputation proxy.
# --------------------------------------------------

df["Academic_Reputation_Score"] = df["THE_Teaching"]


# --------------------------------------------------
# 9. Research Productivity Index
# --------------------------------------------------
# Convert Research Output categories to scores.
#
# Very High = 4
# High      = 3
# Medium    = 2
# Low       = 1
#
# "Very high" is standardized to "Very High".
# --------------------------------------------------

research_output_map = {
    "Very High": 4,
    "Very high": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

df["Research_Output_Score"] = (
    df["Research_Output"]
    .astype("string")
    .str.strip()
    .map(research_output_map)
)

df["Research_Productivity_Index"] = (
    df["Research_Output_Score"] /
    df["Faculty_Count"]
)


# --------------------------------------------------
# 10. Remove temporary calculation columns
# --------------------------------------------------

df = df.drop(
    columns=[
        "QS_Rank_Numeric",
        "THE_Rank_Numeric",
        "QS_Rank_Score",
        "THE_Rank_Score",
        "Estimated_Total_Students",
        "Research_Output_Score"
    ]
)


# --------------------------------------------------
# 11. Round KPI values
# --------------------------------------------------

kpi_columns = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

df[kpi_columns] = df[kpi_columns].round(2)


# --------------------------------------------------
# 12. Save final Excel dataset
# --------------------------------------------------

df.to_excel(
    "university_final_dataset.xlsx",
    index=False
)


# --------------------------------------------------
# 13. Verification
# --------------------------------------------------

print("\nKPI generation completed successfully.")

print("Final dataset shape:", df.shape)

print("\nNew KPI columns:")

for column in kpi_columns:
    print("-", column)

print("\nMissing KPI values:")
print(df[kpi_columns].isnull().sum())

print("\nFinal dataset saved as:")
print("university_final_dataset.xlsx")