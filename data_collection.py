import pandas as pd

# Load QS dataset
qs = pd.read_excel("SABARI'S DATASET 10.xlsx")

# Load THE dataset
the = pd.read_excel("MODIFIED WORLD RANKING DATASET 1.xlsx")

# Add source information
qs["Source"] = "QS"
the["Source"] = "THE"

# Combine QS and THE datasets
raw_data = pd.concat([qs, the], ignore_index=True)

# Save raw combined dataset
raw_data.to_csv("university_raw_data.csv", index=False)

print("Raw dataset created successfully!")
print("Shape:", raw_data.shape)