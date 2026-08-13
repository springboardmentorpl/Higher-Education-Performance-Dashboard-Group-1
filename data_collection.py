import pandas as pd

# ==========================================
# 1. LOAD DATASETS
# ==========================================

qs = pd.read_csv("QS_rankings.csv")
the = pd.read_csv("THE_rankings.csv")


# ==========================================
# 2. KEEP ONLY QS 2022
# ==========================================

qs_2022 = qs[qs["year"] == 2022].copy()


# ==========================================
# 3. CLEAN UNIVERSITY NAMES
# ==========================================

qs_2022["university"] = (
    qs_2022["university"]
    .astype(str)
    .str.strip()
)

the["Name"] = (
    the["Name"]
    .astype(str)
    .str.strip()
)


# ==========================================
# 4. CLEAN COUNTRY NAMES
# ==========================================

qs_2022["country"] = (
    qs_2022["country"]
    .astype(str)
    .str.strip()
)

the["Country"] = (
    the["Country"]
    .astype(str)
    .str.strip()
)


# ==========================================
# 5. STANDARDIZE UNIVERSITY NAMES
# ==========================================

# QS
qs_2022["University_Standard"] = (
    qs_2022["university"]
    .str.replace(r"\s*\(MIT\)$", "", regex=True)
    .str.replace(r"\s*\(Caltech\)$", "", regex=True)
    .str.strip()
)

# THE
the["University_Standard"] = (
    the["Name"]
    .str.replace(r"^The\s+", "", regex=True)
    .str.strip()
)


# ==========================================
# 6. CREATE COMMON COUNTRY COLUMN
# ==========================================

the["country"] = the["Country"]


# ==========================================
# 7. CHECK COLUMNS BEFORE MERGING
# ==========================================

print("QS merge columns:")
print(qs_2022[["University_Standard", "country"]].head())

print("\nTHE merge columns:")
print(the[["University_Standard", "country"]].head())


# ==========================================
# 8. MERGE QS AND THE
# ==========================================

merged_data = pd.merge(
    qs_2022,
    the,
    on=["University_Standard", "country"],
    how="inner",
    suffixes=("_QS", "_THE")
)


# ==========================================
# 9. CHECK MERGED DATASET
# ==========================================

print("\nQS 2022 shape:", qs_2022.shape)
print("THE shape:", the.shape)
print("Merged dataset shape:", merged_data.shape)

print("\nFirst 5 merged records:")
print(merged_data.head())


# ==========================================
# 10. SAVE MERGED DATASET
# ==========================================

merged_data.to_csv(
    "university_raw_data.csv",
    index=False
)

print("\nUniversity raw dataset created successfully.")