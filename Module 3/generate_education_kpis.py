import pandas as pd

# Load final cleaned dataset
df = pd.read_csv("university_cleaned.csv")


# 1. Global Ranking Score
df["Global Ranking Score"] = df["Rank_Normalized"] * 100


# 2. Research Impact Score
df["Research Impact Score"] = df[
    [
        "Research Score",
        "Citations Score",
        "Citations per Faculty Score"
    ]
].mean(axis=1)


# 3. Faculty-to-Student Ratio
df["Faculty-to-Student Ratio"] = df["Student Staff Ratio"]


# 4. International Student Percentage
df["International Student Percentage"] = df["International Students %"]


# 5. Academic Reputation Score
df["Academic Reputation KPI"] = df["Academic Reputation Score"]


# 6. Research Productivity Index
df["Research Productivity Index"] = df[
    [
        "Research Score",
        "International Research Network Score",
        "Citations per Faculty Score"
    ]
].mean(axis=1)


# Save final KPI dataset
df.to_excel(
    "university_final_dataset.xlsx",
    index=False
)


# Display results
print("Module 3 completed successfully!")
print("Dataset shape:", df.shape)

print("\nKPIs created:")
print("1. Global Ranking Score")
print("2. Research Impact Score")
print("3. Faculty-to-Student Ratio")
print("4. International Student Percentage")
print("5. Academic Reputation KPI")
print("6. Research Productivity Index")