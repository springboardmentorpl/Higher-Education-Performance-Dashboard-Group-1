import pandas as pd
from pathlib import Path

# Get project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

print("=" * 55)
print("MODULE 2: DATA CLEANING")
print("=" * 55)

# Load datasets
qs = pd.read_csv(
    DATA_DIR / "qs_rankings_2024.csv",
    encoding="utf-8"
)

the = pd.read_excel(
    DATA_DIR / "world_rankings_cleaned.xlsx"
)

print("QS:", qs.shape)
print("THE:", the.shape)

# Remove duplicate universities
qs = qs.drop_duplicates("Institution_name")
the = the.drop_duplicates("Institution_name")

# Keep only universities present in both datasets
df = pd.merge(
    qs,
    the,
    on="Institution_name",
    how="inner",
    suffixes=("_QS", "_THE")
)

print("Common universities:", len(df))


# -------------------------------------------------------------
# MISSING VALUES BEFORE CLEANING
# -------------------------------------------------------------

before_missing = df.isna().sum().sum()
total_cells = df.shape[0] * df.shape[1]
before_percentage = (before_missing / total_cells) * 100

print("\n========== MISSING VALUES BEFORE CLEANING ==========")
print("Missing cells:", before_missing)
print(f"Missing percentage: {before_percentage:.2f}%")


# -------------------------------------------------------------
# COUNTRY
# -------------------------------------------------------------

df["Country"] = (
    df["location_QS"]
    .fillna(df["location_THE"])
)


# -------------------------------------------------------------
# CATEGORICAL VALUES
# -------------------------------------------------------------

categorical_cols = [
    "SIZE",
    "FOCUS",
    "RESEARCH",
    "STATUS"
]

for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")


# -------------------------------------------------------------
# NUMERICAL VALUES
# -------------------------------------------------------------

numeric_cols = [
    "AGE",
    "stats_number_students",
    "stats_student_staff_ratio",
    "stats_pc_intl_students",
    "stats_female_male_ratio"
]

for col in numeric_cols:

    if col in df.columns:

        if col == "stats_pc_intl_students":
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
            )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        df[col] = df[col].fillna(
            df[col].median()
        )


# -------------------------------------------------------------
# PERFORMANCE SCORES
# -------------------------------------------------------------

score_cols = [
    "Academic Reputation Score",
    "Employer Reputation Score",
    "Faculty Student Score",
    "Citations per Faculty Score",
    "International Faculty Score",
    "International Students Score",
    "International Research Network Score",
    "Employment Outcomes Score",
    "Sustainability Score",
    "scores_teaching",
    "scores_research",
    "scores_citations",
    "scores_industry_income",
    "scores_international_outlook",
    "scores_overall_QS",
    "scores_overall_THE"
]

for col in score_cols:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        df[col] = df[col].fillna(
            df[col].median()
        )


# -------------------------------------------------------------
# RANKINGS
# -------------------------------------------------------------

rank_cols = [
    "rank",
    "2023 RANK",
    "Academic Reputation Rank",
    "Employer Reputation Rank",
    "Faculty Student Rank",
    "Citations per Faculty Rank",
    "International Faculty Rank",
    "International Students Rank",
    "International Research Network Rank",
    "Employment Outcomes Rank",
    "Sustainability Rank",
    "Rank",
    "scores_overall_rank",
    "scores_teaching_rank",
    "scores_research_rank",
    "scores_citations_rank",
    "scores_industry_income_rank",
    "scores_international_outlook_rank"
]


def clean_rank(value):

    if pd.isna(value):
        return None

    value = str(value).strip()
    value = value.replace("+", "").replace("=", "")

    # Convert ranges such as 100-200 to their midpoint
    if "-" in value:
        try:
            low, high = value.split("-", 1)
            return (float(low) + float(high)) / 2
        except:
            return None

    try:
        return float(value)
    except:
        return None


for col in rank_cols:

    if col in df.columns:

        df[col] = df[col].apply(clean_rank)

        df[col] = df[col].fillna(
            df[col].median()
        )


# -------------------------------------------------------------
# FINAL VALIDATION
# -------------------------------------------------------------

print("\n" + "=" * 55)
print("FINAL VALIDATION")
print("=" * 55)

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Duplicate rows:", df.duplicated().sum())

print(
    "Duplicate universities:",
    df["Institution_name"].duplicated().sum()
)

after_missing = df.isna().sum().sum()

after_percentage = (
    after_missing /
    (df.shape[0] * df.shape[1])
) * 100

print(
    f"Missing values: {after_missing} "
    f"({after_percentage:.2f}%)"
)


# -------------------------------------------------------------
# SAVE CLEANED DATASET
# -------------------------------------------------------------

df.to_csv(
    DATA_DIR / "university_cleaned.csv",
    index=False
)

print("\nSaved: university_cleaned.csv")
print("\nModule 2 completed!")