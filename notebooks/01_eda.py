import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned/university_rankings_cleaned.csv")

print("=" * 60)
print("EDUVISION UNIVERSITY RANKINGS - EDA")
print("=" * 60)

# Basic information
print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. DATA TYPES")
print(df.dtypes)

# Missing values
print("\n3. MISSING VALUES")
missing = df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)
print(missing)

# Country analysis
print("\n4. TOP 15 COUNTRIES BY NUMBER OF UNIVERSITIES")
country_counts = df["Country"].value_counts().head(15)
print(country_counts)

# Top universities
print("\n5. TOP 20 UNIVERSITIES - 2024")
top20 = df.sort_values("2024_RANK").head(20)

print(
    top20[
        ["2024_RANK", "Institution_Name", "Country", "Overall_SCORE"]
    ].to_string(index=False)
)

# Biggest rank improvements
df["Rank_Change"] = df["2023_RANK"] - df["2024_RANK"]

print("\n6. BIGGEST RANK IMPROVEMENTS")
improved = df.sort_values("Rank_Change", ascending=False).head(15)

print(
    improved[
        [
            "Institution_Name",
            "Country",
            "2023_RANK",
            "2024_RANK",
            "Rank_Change",
        ]
    ].to_string(index=False)
)

# Biggest rank declines
print("\n7. BIGGEST RANK DECLINES")
declined = df.sort_values("Rank_Change").head(15)

print(
    declined[
        [
            "Institution_Name",
            "Country",
            "2023_RANK",
            "2024_RANK",
            "Rank_Change",
        ]
    ].to_string(index=False)
)

# Country average score
print("\n8. TOP COUNTRIES BY AVERAGE OVERALL SCORE")

country_score = (
    df.groupby("Country")["Overall_SCORE"]
    .agg(["count", "mean"])
    .sort_values("mean", ascending=False)
)

print(country_score.head(15))

# Score statistics
print("\n9. OVERALL SCORE STATISTICS")
print(df["Overall_SCORE"].describe())

print("\nEDA COMPLETE")