"""
University Rankings Analysis - QS vs THE (2024/2025)
------------------------------------------------------
Run this entire script in one go (instead of running notebook cells
one by one). It will print all outputs to the console, save all
charts as PNG image files in the same folder, and save the final
cleaned dataset as a CSV.

Usage:
    python university_rankings_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # saves plots to files instead of needing a popup window
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# display() only exists in Jupyter -- define a plain-Python fallback so this
# script works outside notebooks too.
def display(x):
    print(x)
    print()


# ======================================================================
# Cell 1 — Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

print("Libraries imported successfully")


# ======================================================================
# Cell 2 — Load dataset
df = pd.read_excel("Merged_QS_THE_Universities.xlsx")

print("Dataset Shape:", df.shape)
display(df.head())


# ======================================================================
# Cell 3 — Check dataset information
df.info()


# ======================================================================
# Cell 4 — Check column names
print(df.columns.tolist())


# ======================================================================
# Cell 5 — Standardize column names
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

print(df.columns.tolist())


# ======================================================================
# Cell 6 — Set important column names
# Based on the actual columns in this dataset (from Cell 4/5 output)
QS_NAME_COL   = "qs_institution_name"
QS_RANK_COL   = "qs_2025_rank"
QS_LOC_COL    = "qs_location"

THE_NAME_COL  = "the_name"
THE_RANK_COL  = "the_rank"
THE_LOC_COL   = "the_location"

print("Using QS name/rank:", QS_NAME_COL, QS_RANK_COL)
print("Using THE name/rank:", THE_NAME_COL, THE_RANK_COL)


# ======================================================================
# Cell 7 — Clean university names
df[QS_NAME_COL] = (
    df[QS_NAME_COL]
    .astype("string")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

df[THE_NAME_COL] = (
    df[THE_NAME_COL]
    .astype("string")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print("University names cleaned successfully.")


# ======================================================================
# Cell 8 — Check records before cleaning
print("Records before cleaning:", len(df))
print("Duplicate Records:", df.duplicated().sum())

print("\nMissing values in key columns:")
display(df[[QS_NAME_COL, QS_RANK_COL, THE_NAME_COL, THE_RANK_COL]].isnull().sum())


# ======================================================================
# Cell 9 — Remove duplicate records
before = len(df)
df = df.drop_duplicates().copy()
print("Records before:", before, "| Records after duplicate removal:", len(df))


# ======================================================================
# Cell 10 — Convert ranking columns to numeric
# QS and THE both publish RANGE ranks for lower-ranked universities
# (e.g. "601-610", "1201\u20131500", "1501+"), plus THE uses "Reporter" for
# institutions that submitted data but weren't ranked. This function
# converts each rank into a usable number by taking the midpoint of any
# range, so every university gets one numeric rank we can plot and compare.

def parse_rank(value):
    if pd.isna(value):
        return np.nan
    s = str(value).strip()
    if s.lower() == "reporter":
        return np.nan
    s = s.replace("\u2013", "-").replace("\u2014", "-")  # normalize en/em dashes
    if "+" in s:
        digits = "".join(ch for ch in s if ch.isdigit())
        return float(digits) if digits else np.nan
    if "-" in s:
        parts = [p for p in s.split("-") if p.strip().isdigit()]
        if len(parts) == 2:
            lo, hi = float(parts[0]), float(parts[1])
            return (lo + hi) / 2
    try:
        return float(s)
    except ValueError:
        return np.nan

# Keep the original text (e.g. "601-610") alongside the numeric estimate
df["qs_rank_band"] = df[QS_RANK_COL].astype(str)
df["the_rank_band"] = df[THE_RANK_COL].astype(str)

df["qs_rank_clean"] = df[QS_RANK_COL].apply(parse_rank)
df["the_rank_clean"] = df[THE_RANK_COL].apply(parse_rank)

print(df["qs_rank_clean"].dtype, df["the_rank_clean"].dtype)
display(df[[QS_RANK_COL, "qs_rank_clean", THE_RANK_COL, "the_rank_clean"]].head(10))


# ======================================================================
# Cell 11 — University name column (for downstream display)
df["university_name"] = df[QS_NAME_COL].fillna(df[THE_NAME_COL])

print("University name column created.")
print("Missing names after fallback:", df["university_name"].isnull().sum())


# ======================================================================
# Cell 12 — Rank difference
df["rank_difference"] = df["the_rank_clean"] - df["qs_rank_clean"]
df["absolute_rank_difference"] = df["rank_difference"].abs()

display(
    df[["university_name", "qs_rank_clean", "the_rank_clean",
        "rank_difference", "absolute_rank_difference"]].head(10)
)


# ======================================================================
# Cell 13 — Create ranking categories
def rank_category(rank):
    if pd.isna(rank):
        return "Unknown"
    elif rank <= 10:
        return "Top 10"
    elif rank <= 50:
        return "11-50"
    elif rank <= 100:
        return "51-100"
    elif rank <= 500:
        return "101-500"
    else:
        return "Above 500"

df["qs_rank_category"] = df["qs_rank_clean"].apply(rank_category)
df["the_rank_category"] = df["the_rank_clean"].apply(rank_category)

print("QS Ranking Categories:")
display(df["qs_rank_category"].value_counts())

print("THE Ranking Categories:")
display(df["the_rank_category"].value_counts())


# ======================================================================
# Cell 14 — Compare QS and THE
def ranking_comparison(row):
    qs_rank = row["qs_rank_clean"]
    the_rank = row["the_rank_clean"]

    if pd.isna(qs_rank) or pd.isna(the_rank):
        return "Unavailable"
    elif qs_rank < the_rank:
        return "QS Higher"
    elif qs_rank > the_rank:
        return "THE Higher"
    else:
        return "Same Rank"

df["ranking_comparison"] = df.apply(ranking_comparison, axis=1)

display(df["ranking_comparison"].value_counts())


# ======================================================================
# Cell 15 — Check missing values after processing
missing = df.isnull().sum().sort_values(ascending=False)
display(missing[missing > 0].head(20))


# ======================================================================
# Cell 16 — Handle missing values (numeric columns used in analysis)
for col in ["qs_rank_clean", "the_rank_clean", "rank_difference", "absolute_rank_difference"]:
    missing_before = df[col].isnull().sum()
    df[col] = df[col].fillna(df[col].median())
    print(f"{col}: filled {missing_before} missing values with median")


# ======================================================================
# Cell 17 — Final dataset validation
print("Final Number of Records:", len(df))
print("Final Number of Columns:", len(df.columns))
print("Duplicate Records:", df.duplicated().sum())


# ======================================================================
# Cell 18 — KPI calculation
total_universities = df["university_name"].nunique()
average_qs_rank = df["qs_rank_clean"].mean()
average_the_rank = df["the_rank_clean"].mean()
average_rank_difference = df["absolute_rank_difference"].mean()
number_of_countries = df[THE_LOC_COL].nunique()

print("========== KPI ANALYSIS ==========")
print("Total Universities:", total_universities)
print("Average QS Rank:", round(average_qs_rank, 2))
print("Average THE Rank:", round(average_the_rank, 2))
print("Average Absolute Rank Difference:", round(average_rank_difference, 2))
print("Number of Countries:", number_of_countries)


# ======================================================================
# Cell 19 — KPI table
kpis = {
    "Total Universities": total_universities,
    "Average QS Rank": round(average_qs_rank, 2),
    "Average THE Rank": round(average_the_rank, 2),
    "Average Rank Difference": round(average_rank_difference, 2),
    "Number of Countries": number_of_countries,
}

kpi_table = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
display(kpi_table)


# ======================================================================
# Cell 20 — Top 10 QS universities
top_qs = df.sort_values("qs_rank_clean")[["university_name", "qs_rank_clean"]].head(10)
display(top_qs)


# ======================================================================
# Cell 21 — Top 10 THE universities
top_the = df.sort_values("the_rank_clean")[["university_name", "the_rank_clean"]].head(10)
display(top_the)


# ======================================================================
# Cell 22 — Largest ranking differences
largest_difference = (
    df.sort_values("absolute_rank_difference", ascending=False)
    [["university_name", "qs_rank_clean", "the_rank_clean",
      "rank_difference", "absolute_rank_difference"]]
    .head(10)
)
display(largest_difference)


# ======================================================================
# Cell 23 — QS vs THE scatter plot
plot_data = df.dropna(subset=["qs_rank_clean", "the_rank_clean"])

plt.figure(figsize=(8, 6))
plt.scatter(plot_data["qs_rank_clean"], plot_data["the_rank_clean"], alpha=0.5)
plt.xlabel("QS Rank")
plt.ylabel("THE Rank")
plt.title("QS Rank vs THE Rank")
plt.grid(alpha=0.2)
plt.savefig("chart_1.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_1.png")


# ======================================================================
# Cell 24 — Rank difference distribution
plt.figure(figsize=(10, 6))
plt.hist(df["rank_difference"].dropna(), bins=30)
plt.xlabel("THE Rank - QS Rank")
plt.ylabel("Number of Universities")
plt.title("Distribution of QS vs THE Rank Differences")
plt.savefig("chart_2.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_2.png")


# ======================================================================
# Cell 25 — QS ranking categories
category_counts = df["qs_rank_category"].value_counts()

plt.figure(figsize=(8, 5))
category_counts.plot(kind="bar")
plt.xlabel("QS Ranking Category")
plt.ylabel("Number of Universities")
plt.title("Universities by QS Ranking Category")
plt.xticks(rotation=0)
plt.savefig("chart_3.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_3.png")


# ======================================================================
# Cell 26 — THE ranking categories
the_category_counts = df["the_rank_category"].value_counts()

plt.figure(figsize=(8, 5))
the_category_counts.plot(kind="bar")
plt.xlabel("THE Ranking Category")
plt.ylabel("Number of Universities")
plt.title("Universities by THE Ranking Category")
plt.xticks(rotation=0)
plt.savefig("chart_4.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_4.png")


# ======================================================================
# Cell 27 — Correlation
correlation = df[["qs_rank_clean", "the_rank_clean"]].corr()
display(correlation)


# ======================================================================
# Cell 28 — Correlation heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(correlation, annot=True, fmt=".2f")
plt.title("Correlation Between QS and THE Rankings")
plt.savefig("chart_5.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_5.png")


# ======================================================================
# Cell 29 — Country analysis
country_counts = df[THE_LOC_COL].value_counts().head(10)
display(country_counts)


# ======================================================================
# Cell 30 — Country visualization
plt.figure(figsize=(10, 6))
country_counts.plot(kind="bar")
plt.xlabel("Country")
plt.ylabel("Number of Universities")
plt.title("Top 10 Countries by Number of Universities")
plt.xticks(rotation=45, ha="right")
plt.savefig("chart_6.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()
print("Saved chart as chart_6.png")


# ======================================================================
# Cell 31 — Save final dataset
final_dataset = df.copy()
final_dataset.to_csv("final_cleaned_university_dataset.csv", index=False)

print("Final dataset saved as 'final_cleaned_university_dataset.csv'")
print("Final dataset shape:", final_dataset.shape)


# ======================================================================
# Cell 32 — Display final dataset
display(final_dataset.head(20))


# ======================================================================
# Cell 33 — Final summary
print("========== PROJECT SUMMARY ==========")
print("Total Records:", len(final_dataset))
print("Total Columns:", len(final_dataset.columns))
print("Duplicate Records:", final_dataset.duplicated().sum())
print("\nProject completed successfully!")
