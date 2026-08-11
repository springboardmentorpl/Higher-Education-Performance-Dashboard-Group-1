import pandas as pd
import os

def collect_and_merge_datasets(wur_path: str, qs_path: str, output_path: str) -> pd.DataFrame:
    """
    Loads raw university ranking datasets, standardizes structural column names,
    applies provenance tags, and merges them into a raw unified dataset.
    """
    print("[1/3] Loading raw datasets...")
    df_wur = pd.read_csv(wur_path)
    df_qs = pd.read_csv(qs_path)

    # Align QS rank column header with standard schema
    if 'qs rank' in df_qs.columns:
        df_qs = df_qs.rename(columns={'qs rank': 'rank'})

    # Tag provenance for downstream filtering and comparative analytics
    df_wur['ranking_source'] = 'THE World University Rankings 2024'
    df_qs['ranking_source'] = 'QS World University Rankings 2026'

    # Append datasets into a unified structure
    df_merged = pd.concat([df_wur, df_qs], ignore_index=True)
    
    # Save combined raw data
    df_merged.to_csv(output_path, index=False)
    print(f"[SUCCESS] Merged raw dataset saved to '{output_path}' ({df_merged.shape[0]} rows, {df_merged.shape[1]} columns).")
    return df_merged

if __name__ == "__main__":
    WUR_FILE = "World_University_Rating_2024.csv"
    QS_FILE = "2026 QS_Universities_Data.csv"
    RAW_OUTPUT = "university_raw_data.csv"

    if os.path.exists(WUR_FILE) and os.path.exists(QS_FILE):
        collect_and_merge_datasets(WUR_FILE, QS_FILE, RAW_OUTPUT)
    else:
        print("Error: Input files not found in the working directory.")