import pandas as pd

INPUT_FILE = "data/cleaned/university_rankings_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("EDUVISION - DATA QUALITY ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# 1. Missing values percentage
# --------------------------------------------------

missing = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percentage": (df.isna().mean() * 100).round(2)
})

missing = missing[missing["Missing_Count"] > 0]
missing = missing.sort_values("Missing_Count", ascending=False)

print("\n1. MISSING VALUE SUMMARY")
print(missing.to_string())

# --------------------------------------------------
# 2. Valid ranking records
# --------------------------------------------------

ranked = df[df["2024_RANK"].notna()].copy()

print("\n2. VALID 2024 RANKING RECORDS")
print("Rows:", len(ranked))

# --------------------------------------------------
# 3. Valid score records
# --------------------------------------------------

scored = df[df["Overall_SCORE"].notna()].copy()

print("\n3. VALID OVERALL SCORE RECORDS")
print("Rows:", len(scored))

# --------------------------------------------------
# 4. Ranked + scored universities
# --------------------------------------------------

complete_ranking = df[
    df["2024_RANK"].notna() &
    df["Overall_SCORE"].notna()
].copy()

print("\n4. RANKED + SCORED UNIVERSITIES")
print("Rows:", len(complete_ranking))

# --------------------------------------------------
# 5. Top 20 based on valid 2024 rank
# --------------------------------------------------

print("\n5. TOP 20 UNIVERSITIES")

top20 = (
    complete_ranking
    .sort_values("2024_RANK")
    .head(20)
)

print(
    top20[
        [
            "2024_RANK",
            "Institution_Name",
            "Country",
            "Overall_SCORE"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# 6. Countries with most ranked universities
# --------------------------------------------------

print("\n6. COUNTRIES WITH MOST RANKED UNIVERSITIES")

country_ranked = (
    ranked["Country"]
    .value_counts()
    .head(20)
)

print(country_ranked.to_string())

# --------------------------------------------------
# 7. Score distribution
# --------------------------------------------------

print("\n7. OVERALL SCORE DISTRIBUTION")

score_bins = pd.cut(
    scored["Overall_SCORE"],
    bins=[0, 20, 40, 60, 80, 100],
    labels=[
        "0-20",
        "20-40",
        "40-60",
        "60-80",
        "80-100"
    ],
    include_lowest=True
)

print(score_bins.value_counts().sort_index())

# --------------------------------------------------
# 8. Missingness of important metrics
# --------------------------------------------------

important_columns = [
    "Academic_Reputation_Score",
    "Employer_Reputation_Score",
    "Faculty_Student_Score",
    "Citations_per_Faculty_Score",
    "International_Faculty_Score",
    "International_Students_Score",
    "International_Research_Network_Score",
    "Employment_Outcomes_Score",
    "Sustainability_Score",
    "Overall_SCORE"
]

print("\n8. IMPORTANT METRIC COMPLETENESS")

for column in important_columns:
    valid = df[column].notna().sum()
    percentage = valid / len(df) * 100

    print(
        f"{column:45} "
        f"{valid:4} valid "
        f"({percentage:6.2f}%)"
    )

print("\nDATA QUALITY ANALYSIS COMPLETE")