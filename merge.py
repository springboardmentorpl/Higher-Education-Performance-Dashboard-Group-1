import pandas as pd
import os



downloads = os.path.join(os.path.expanduser("~"), "Downloads")


cwur_file = os.path.join(downloads, "cwurData.csv")
qs_file = os.path.join(downloads, "2026 QS World University Rankings.csv")


cwur = pd.read_csv(cwur_file)
qs = pd.read_csv(qs_file)

print("CWUR Dataset Loaded Successfully")
print("CWUR Shape:", cwur.shape)

print("\nQS Dataset Loaded Successfully")
print("QS Shape:", qs.shape)


print("\nCWUR Columns:")
print(cwur.columns.tolist())

print("\nQS Columns:")
print(qs.columns.tolist())

qs.rename(columns={
    "Institution Name": "University Name",
    "Country/Territory": "Country"
}, inplace=True)



required_columns = ["University Name", "Country"]

for column in required_columns:

    if column not in cwur.columns:
        print(f"CWUR does not contain: {column}")

    if column not in qs.columns:
        print(f"QS does not contain: {column}")
=

cwur["University Name"] = cwur["University Name"].astype(str)
qs["University Name"] = qs["University Name"].astype(str)

cwur["Country"] = cwur["Country"].astype(str)
qs["Country"] = qs["Country"].astype(str)


cwur["University Name"] = (
    cwur["University Name"]
    .str.strip()
)

qs["University Name"] = (
    qs["University Name"]
    .str.strip()
)

cwur["Country"] = (
    cwur["Country"]
    .str.strip()
)

qs["Country"] = (
    qs["Country"]
    .str.strip()
)



cwur["University Name"] = (
    cwur["University Name"]
    .str.lower()
)

qs["University Name"] = (
    qs["University Name"]
    .str.lower()
)

cwur["Country"] = (
    cwur["Country"]
    .str.lower()
)

qs["Country"] = (
    qs["Country"]
    .str.lower()
)




country_mapping = {

    "usa": "united states",
    "u.s.a.": "united states",
    "us": "united states",
    "united states of america": "united states",

    "uk": "united kingdom",
    "u.k.": "united kingdom",

    "uae": "united arab emirates",
    "u.a.e.": "united arab emirates"

}


cwur["Country"] = cwur["Country"].replace(country_mapping)
qs["Country"] = qs["Country"].replace(country_mapping)




cwur.drop_duplicates(inplace=True)

qs.drop_duplicates(inplace=True)




cwur.dropna(
    subset=["University Name", "Country"],
    inplace=True
)

qs.dropna(
    subset=["University Name", "Country"],
    inplace=True
)




merged = pd.merge(

    cwur,

    qs,

    on=[
        "University Name",
        "Country"
    ],

    how="inner",

    suffixes=("_CWUR", "_QS")
)




print("\n====================================")
print("MERGE SUCCESSFUL")
print("====================================")

print("Merged Dataset Shape:", merged.shape)

print("\nNumber of Rows:", merged.shape[0])
print("Number of Columns:", merged.shape[1])



print("\nFirst 10 Records:")

print(
    merged.head(10).to_string(index=False)
)




print("\nMerged Dataset Columns:")

print(
    merged.columns.tolist()
)




output_file = os.path.join(
    downloads,
    "Merged_University_Rankings.csv"
)

merged.to_csv(
    output_file,
    index=False
)


print("\n====================================")
print("FILE SAVED SUCCESSFULLY")
print("====================================")

print("File location:")
print(output_file)