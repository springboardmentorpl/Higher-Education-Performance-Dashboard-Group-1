import pandas as pd
import numpy as np
import re
input_file = "university_cleaned_data.csv"
df = pd.read_csv(input_file)
print("Original Shape:", df.shape)
numeric_columns = [
    "QS Citation Score",
    "THE Citation Score",
    "Student Staff Ratio",
    "Number of Students",
    "International Students %",
    "Academic Reputation",
    "Research Score"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col],errors="coerce")
def rank_start(value):
    if pd.isna(value):
        return np.nan
    value = str(value).strip()
    match = re.search(r"\d+", value)
    if match:
        return int(match.group())
    return np.nan
df["QS Rank Numeric"] = df["QS Rank"].apply(rank_start)
df["THE Rank Numeric"] = df["THE Rank"].apply(rank_start)
qs_max_rank = df["QS Rank Numeric"].max()
the_max_rank = df["THE Rank Numeric"].max()
df["QS Rank Score"] = (100 * (qs_max_rank - df["QS Rank Numeric"] + 1) / qs_max_rank)
df["THE Rank Score"] = (100 * (the_max_rank - df["THE Rank Numeric"] + 1) / the_max_rank)
df["Global Ranking Score"] = (df["QS Rank Score"].combine_first(df["THE Rank Score"]))
both_available = (df["QS Rank Score"].notna()&df["THE Rank Score"].notna())
df.loc[both_available, "Global Ranking Score"] = ((df.loc[both_available, "QS Rank Score"]+df.loc[both_available, "THE Rank Score"]) / 2)
df["Global Ranking Score"] = (df["Global Ranking Score"].round(2))
df["Research Impact Score"] = ((df["QS Citation Score"]+df["THE Citation Score"]) / 2).round(2)
df["Faculty-to-Student Ratio"] = (df["Student Staff Ratio"].round(2))
df["International Student Percentage"] = (df["International Students %"].round(2))
df["Academic Reputation Score"] = (df["Academic Reputation"].round(2))
df["Research Performance"] = (0.5 * df["Research Score"]+0.5 * df["Research Impact Score"])
df["Research Productivity Raw"] = (df["Research Performance"]/np.sqrt(df["Number of Students"]))
min_productivity = df["Research Productivity Raw"].min()
max_productivity = df["Research Productivity Raw"].max()
if max_productivity != min_productivity:
    df["Research Productivity Index"] = (100*(df["Research Productivity Raw"] -min_productivity)/(max_productivity-min_productivity)).round(2)
else:
    df["Research Productivity Index"] = 100.0
temporary_columns = [
    "QS Rank Score",
    "THE Rank Score",
    "QS Rank Numeric",
    "THE Rank Numeric",
    "Research Performance",
    "Research Productivity Raw"
]
df.drop(columns=temporary_columns,inplace=True)
kpi_columns = [
    "Global Ranking Score",
    "Research Impact Score",
    "Faculty-to-Student Ratio",
    "International Student Percentage",
    "Academic Reputation Score",
    "Research Productivity Index"
]
print("\n" + "=" * 70)
print("KPI RESULTS")
print("=" * 70)
print(df[["University Name"] + kpi_columns].head(20))
print("\n" + "=" * 70)
print("KPI MISSING VALUES")
print("=" * 70)
print(df[kpi_columns].isnull().sum())
output_file = "university_final_dataset.xlsx"
df.to_excel(output_file,index=False)
print("\n" + "=" * 70)
print("KPI ENGINEERING COMPLETED")
print("=" * 70)
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])
print("Saved   :", output_file)
print("=" * 70)