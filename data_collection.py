import pandas as pd

def collect_and_merge_data():
    print("Loading datasets...")
    
    # 1. Load the raw datasets using utf-8 encoding to prevent scrambled text
    qs_df = pd.read_csv('2024 QS World University Rankings.csv', encoding='utf-8') 
    the_df = pd.read_csv('2024_rankings.csv', encoding='utf-8') 

    print("Merging datasets...")
    
    # 2. Merge the datasets
    merged_df = pd.merge(
        qs_df, 
        the_df, 
        left_on='Institution Name', 
        right_on='name', 
        how='outer'
    )

    # 3. Save the final deliverable using utf-8-sig so Excel reads it perfectly
    merged_df.to_csv('university_raw_data.csv', index=False, encoding='utf-8-sig')
    print("Merge successful! File saved as university_raw_data.csv")

if __name__ == "__main__":
    collect_and_merge_data()