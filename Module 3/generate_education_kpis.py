import pandas as pd
import numpy as np

def generate_education_kpis(input_csv: str, output_excel: str, output_csv: str):
    """
    Computes global higher education performance indicators and exports
    a Tableau-ready dataset.
    """
    print("[1/2] Loading cleaned dataset...")
    df = pd.read_csv(input_csv)

    print("[2/2] Calculating Higher Education KPIs...")

    # KPI 1: Global Ranking Score (Cleaned Overall Performance Score)
    df['KPI_Global_Ranking_Score'] = df['scores_overall'].round(2)

    # KPI 2: Research Impact Score (Weighted combo of research activity & citation influence)
    df['KPI_Research_Impact_Score'] = (
        (0.4 * df['scores_research']) + (0.6 * df['scores_citations'])
    ).round(2)

    # KPI 3: Faculty-to-Student Ratio (Calculated as faculty count per student: 1 / student_staff_ratio)
    df['KPI_Faculty_To_Student_Ratio'] = np.where(
        df['stats_student_staff_ratio_clean'] > 0,
        (1.0 / df['stats_student_staff_ratio_clean']).round(4),
        np.nan
    )

    # KPI 4: International Student Percentage (%)
    df['KPI_International_Student_Pct'] = df['stats_pc_intl_students_clean'].round(2)

    # KPI 5: Academic Reputation Score (Derived from Teaching Excellence Score)
    df['KPI_Academic_Reputation_Score'] = df['scores_teaching'].round(2)

    # KPI 6: Research Productivity Index (Composite metric: Research + Citations + Industry Income)
    df['KPI_Research_Productivity_Index'] = (
        (0.50 * df['scores_research']) +
        (0.35 * df['scores_citations']) +
        (0.15 * df['scores_industry_income'])
    ).round(2)

    # Select and organize columns for Tableau import
    kpi_columns = [
        'rank', 'clean_rank', 'name', 'location', 'ranking_source',
        'stats_number_students_clean', 'stats_student_staff_ratio_clean',
        'KPI_Global_Ranking_Score', 'KPI_Research_Impact_Score',
        'KPI_Faculty_To_Student_Ratio', 'KPI_International_Student_Pct',
        'KPI_Academic_Reputation_Score', 'KPI_Research_Productivity_Index',
        'scores_overall', 'scores_teaching', 'scores_research',
        'scores_citations', 'scores_industry_income', 'scores_international_outlook'
    ]
    
    df_tableau = df[kpi_columns].copy()

    # Save final deliverables
    df_tableau.to_excel(output_excel, index=False, engine='openpyxl')
    df_tableau.to_csv(output_csv, index=False)
    
    print(f"[SUCCESS] Final KPI engineered dataset exported to:")
    print(f" - Excel: {output_excel}")
    print(f" - CSV:   {output_csv}")

if __name__ == "__main__":
    generate_education_kpis(
        input_csv="university_cleaned.csv",
        output_excel="university_final_dataset.xlsx",
        output_csv="university_final_dataset.csv"
    )