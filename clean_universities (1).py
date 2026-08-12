"""
University Rankings Dataset Cleaner
------------------------------------
Cleans university_final_dataset_FINAL-1.xlsx:
 1. Removes exact + near-duplicate rows
 2. Standardizes university names
 3. Standardizes country names
 4. Normalizes ranking metrics (0-100 scale, consistent direction)
 5. Exports Tableau-ready CSV files (wide fact table + long-format metrics table)

Usage:
    pip install pandas openpyxl rapidfuzz
    python clean_universities.py

Place this script in the same folder as university_final_dataset_FINAL-1.xlsx
"""

import re
import pandas as pd
import numpy as np
from rapidfuzz import fuzz

INPUT_FILE = r"C:\Users\USER\Downloads\final\university_final_dataset_FINAL (1).xlsx"


df = pd.read_excel(INPUT_FILE, sheet_name="Sheet1")
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")


def clean_name(name: str) -> str:
    """Normalize whitespace/punctuation and strip trailing abbreviations
    such as '(MIT)', '(NUS)', 'UCB', etc. that cause near-duplicates."""
    if pd.isna(name):
        return name
    n = str(name).strip()
    n = re.sub(r"\s+", " ", n)                        # collapse whitespace
    n = n.replace("\u2019", "'").replace("`", "'")     # normalize apostrophes
    n = re.sub(r"\s*\(.*?\)\s*", " ", n).strip()       # drop parenthetical abbreviations
    n = re.sub(r"\s+,", ",", n)                        # fix stray spaces before commas
    n = n.rstrip(",").strip()
    return n

df["university_name_clean"] = df["university_name"].apply(clean_name)
df["university_name_key"] = (
    df["university_name_clean"].str.lower()
    .str.replace(r"[^a-z0-9 ]", "", regex=True)
    .str.strip()
)


COUNTRY_MAP = {
    "usa": "United States", "us": "United States", "u.s.a.": "United States",
    "uk": "United Kingdom", "u.k.": "United Kingdom",
    "uae": "United Arab Emirates",
    "korea, south": "South Korea",
    "hong kong": "Hong Kong SAR China",
    "macau": "Macau SAR China", "macao": "Macau SAR China",
    "russian federation": "Russia",
    "czech republic": "Czechia",
}

def clean_country(c: str) -> str:
    if pd.isna(c):
        return c
    c2 = str(c).strip()
    key = c2.lower()
    return COUNTRY_MAP.get(key, c2)

df["country_clean"] = df["country"].apply(clean_country)


before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} exact duplicate rows")


before = len(df)
df = (
    df.sort_values("global_ranking_score", ascending=False)
      .drop_duplicates(subset=["university_name_key", "country_clean"], keep="first")
)
print(f"Removed {before - len(df)} duplicate (name, country) pairs")


def fuzzy_dedupe(frame: pd.DataFrame, threshold: int = 92) -> pd.DataFrame:
    keep_idx = []
    seen_by_country = {}
    for idx, row in frame.iterrows():
        c = row["country_clean"]
        name = row["university_name_key"]
        bucket = seen_by_country.setdefault(c, [])
        is_dup = any(fuzz.ratio(name, existing) >= threshold for existing in bucket)
        if not is_dup:
            bucket.append(name)
            keep_idx.append(idx)
    return frame.loc[keep_idx]

before = len(df)
df = fuzzy_dedupe(df)
print(f"Removed {before - len(df)} fuzzy near-duplicate rows")


score_cols = [c for c in df.columns if c.endswith("_score") or c.endswith("_index")]
for col in score_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").clip(0, 100)


for rank_col, out_col in [("qs_rank", "qs_rank_norm"), ("arwu_rank", "arwu_rank_norm")]:
    r = pd.to_numeric(df[rank_col], errors="coerce")
    max_r = r.max()
    df[out_col] = np.where(r.notna(), 100 * (1 - (r - 1) / (max_r - 1)), np.nan)
    df[out_col] = df[out_col].round(2)


for col in ["qs_rank_category", "arwu_rank_category"]:
    df[col] = df[col].fillna("Unranked").astype(str).str.strip().str.title()

df["ranking_comparison"] = df["ranking_comparison"].fillna("Not Comparable").astype(str).str.strip()


df = df.rename(columns={"university_name_clean": "university_name_final",
                         "country_clean": "country_final"})

final_cols = [
    "university_name_final", "country_final", "region", "university_size", "focus",
    "research_intensity", "institution_status",
    "global_ranking_score", "qs_published_overall_score",
    "qs_rank", "qs_rank_category", "qs_rank_norm",
    "arwu_rank", "arwu_rank_category", "arwu_rank_norm",
    "rank_difference", "absolute_rank_difference", "ranking_comparison",
    "academic_reputation_score", "employer_reputation_score",
    "faculty_student_ratio_score", "international_student_score",
    "international_faculty_score", "international_student_diversity_score",
    "international_research_network_score", "research_impact_score",
    "research_productivity_index", "employment_outcomes_score",
    "sustainability_score",
    "arwu_overall_score", "arwu_alumni_score", "arwu_award_score",
    "arwu_highly_cited_researchers_score", "arwu_nature_science_score",
    "arwu_publications_score", "arwu_per_capita_score",
]
final_cols = [c for c in final_cols if c in df.columns]
clean_df = df[final_cols].rename(columns={
    "university_name_final": "university_name",
    "country_final": "country",
})

clean_df.insert(0, "university_id", range(1, len(clean_df) + 1))



clean_df.to_csv("universities_clean_wide.csv", index=False)


metric_cols = [c for c in clean_df.columns if c.endswith("_score") or c.endswith("_norm")
               or c.endswith("_index") or c in ("qs_rank", "arwu_rank")]
long_df = clean_df.melt(
    id_vars=["university_id", "university_name", "country", "region"],
    value_vars=metric_cols,
    var_name="metric_name",
    value_name="metric_value",
)
long_df.to_csv("universities_clean_long.csv", index=False)

print(f"\nFinal clean dataset: {len(clean_df)} unique universities")
print("Exported: universities_clean_wide.csv, universities_clean_long.csv")
