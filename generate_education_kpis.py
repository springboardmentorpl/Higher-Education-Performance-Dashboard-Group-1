import pandas as pd
import numpy as np

print("--- Step 1: Loading Dataset ---")
df = pd.read_csv('cleaned_university_data_2024.csv')

def clean_numeric(val):
    if pd.isna(val) or val == 'Unknown' or val == 0:
        return np.nan
    if isinstance(val, str):
        val = val.replace('%', '').replace(',', '').strip()
    try:
        return float(val)
    except:
        return np.nan

print("--- Step 2: Calculating 6 Core KPIs ---")

# 1. Global Ranking Score[cite: 1]
df['temp_qs_overall'] = df['Overall SCORE'].apply(clean_numeric)
df['temp_the_overall'] = df['scores_overall'].apply(clean_numeric)
df['KPI_Global_Ranking_Score'] = df[['temp_qs_overall', 'temp_the_overall']].mean(axis=1)

# 2. Research Impact Score[cite: 1]
df['temp_qs_cite'] = df['Citations per Faculty Score'].apply(clean_numeric)
df['temp_the_cite'] = df['scores_citations'].apply(clean_numeric)
df['KPI_Research_Impact_Score'] = df[['temp_qs_cite', 'temp_the_cite']].mean(axis=1)

# 3. Faculty-to-Student Ratio[cite: 1]
df['KPI_Faculty_Student_Ratio'] = df['stats_student_staff_ratio'].apply(clean_numeric)

# 4. International Student Percentage[cite: 1]
df['KPI_Intl_Student_Pct'] = df['stats_pc_intl_students'].apply(clean_numeric)

# 5. Academic Reputation Score[cite: 1]
df['KPI_Academic_Reputation'] = df['Academic Reputation Score'].apply(clean_numeric)

# 6. Research Productivity Index[cite: 1]
df['temp_the_research'] = df['scores_research'].apply(clean_numeric)
df['temp_qs_network'] = df['International Research Network Score'].apply(clean_numeric)
df['KPI_Research_Productivity'] = df[['temp_the_research', 'temp_qs_network']].mean(axis=1)

print("--- Step 3: Final Power BI Formatting ---")
kpi_columns = [
    'KPI_Global_Ranking_Score', 'KPI_Research_Impact_Score', 
    'KPI_Faculty_Student_Ratio', 'KPI_Intl_Student_Pct', 
    'KPI_Academic_Reputation', 'KPI_Research_Productivity'
]


df[kpi_columns] = df[kpi_columns].round(2)

df = df.drop(columns=['temp_qs_overall', 'temp_the_overall', 'temp_qs_cite', 
                      'temp_the_cite', 'temp_the_research', 'temp_qs_network'])

print("--- Step 4: Exporting Final Excel File ---")
output_file = 'university_final_dataset.xlsx'
df.to_excel(output_file, index=False)

print(f"SUCCESS! Milestone 2 Complete. File saved as: {output_file}")
