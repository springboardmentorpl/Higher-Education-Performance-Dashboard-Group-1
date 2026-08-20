import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# EDUVISION - DATA VISUALIZATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "university_rankings_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data" / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 60)
print("EDUVISION UNIVERSITY RANKINGS - VISUALIZATION")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully")
print("Shape:", df.shape)


# ============================================================
# 2. TOP 20 UNIVERSITIES
# ============================================================

ranked_df = df.dropna(
    subset=["2024_RANK", "Overall_SCORE"]
).sort_values("2024_RANK").head(20)

plt.figure(figsize=(12, 8))

plt.barh(
    ranked_df["Institution_Name"].iloc[::-1],
    ranked_df["Overall_SCORE"].iloc[::-1]
)

plt.xlabel("Overall Score")
plt.ylabel("University")
plt.title("Top 20 Universities - 2024")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_20_universities.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: top_20_universities.png")


# ============================================================
# 3. TOP COUNTRIES BY NUMBER OF RANKED UNIVERSITIES
# ============================================================

country_counts = (
    df.dropna(subset=["2024_RANK"])
    .groupby("Country")
    .size()
    .sort_values(ascending=False)
    .head(15)
)

plt.figure(figsize=(12, 7))

country_counts.sort_values().plot(kind="barh")

plt.xlabel("Number of Universities")
plt.ylabel("Country")
plt.title("Top 15 Countries by Number of Ranked Universities")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_countries_by_universities.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: top_countries_by_universities.png")


# ============================================================
# 4. OVERALL SCORE DISTRIBUTION
# ============================================================

score_data = df["Overall_SCORE"].dropna()

plt.figure(figsize=(10, 6))

plt.hist(score_data, bins=20)

plt.xlabel("Overall Score")
plt.ylabel("Number of Universities")
plt.title("Overall University Score Distribution")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "overall_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: overall_score_distribution.png")


# ============================================================
# 5. RANK VS OVERALL SCORE
# ============================================================

rank_score_df = df.dropna(
    subset=["2024_RANK", "Overall_SCORE"]
)

plt.figure(figsize=(10, 7))

plt.scatter(
    rank_score_df["2024_RANK"],
    rank_score_df["Overall_SCORE"],
    alpha=0.6
)

plt.xlabel("2024 Rank")
plt.ylabel("Overall Score")
plt.title("2024 University Rank vs Overall Score")

plt.gca().invert_xaxis()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "rank_vs_score.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: rank_vs_score.png")


# ============================================================
# 6. TOP COUNTRIES BY AVERAGE SCORE
# ============================================================

country_scores = (
    df.dropna(subset=["Overall_SCORE"])
    .groupby("Country")["Overall_SCORE"]
    .agg(["count", "mean"])
)

country_scores = (
    country_scores[country_scores["count"] >= 5]
    .sort_values("mean", ascending=False)
    .head(15)
)

plt.figure(figsize=(12, 7))

country_scores["mean"].sort_values().plot(kind="barh")

plt.xlabel("Average Overall Score")
plt.ylabel("Country")
plt.title("Top Countries by Average Overall Score")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_countries_average_score.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: top_countries_average_score.png")


# ============================================================
# 7. ACADEMIC REPUTATION VS EMPLOYER REPUTATION
# ============================================================

reputation_df = df.dropna(
    subset=[
        "Academic_Reputation_Score",
        "Employer_Reputation_Score"
    ]
)

plt.figure(figsize=(10, 7))

plt.scatter(
    reputation_df["Academic_Reputation_Score"],
    reputation_df["Employer_Reputation_Score"],
    alpha=0.5
)

plt.xlabel("Academic Reputation Score")
plt.ylabel("Employer Reputation Score")
plt.title("Academic Reputation vs Employer Reputation")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "academic_vs_employer_reputation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: academic_vs_employer_reputation.png")


# ============================================================
# 8. INTERNATIONAL FACULTY VS INTERNATIONAL STUDENTS
# ============================================================

international_df = df.dropna(
    subset=[
        "International_Faculty_Score",
        "International_Students_Score"
    ]
)

plt.figure(figsize=(10, 7))

plt.scatter(
    international_df["International_Faculty_Score"],
    international_df["International_Students_Score"],
    alpha=0.5
)

plt.xlabel("International Faculty Score")
plt.ylabel("International Students Score")
plt.title("International Faculty vs International Students")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "international_faculty_vs_students.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: international_faculty_vs_students.png")


# ============================================================
# 9. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETE")
print("=" * 60)

print("\nVisualization files saved to:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print("-", file.name)

print("\nOutput directory:")
print(OUTPUT_DIR)