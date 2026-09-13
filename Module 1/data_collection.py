# %%
import pandas as pd
import re
import unicodedata
from ftfy import fix_text
from rapidfuzz import process, fuzz
def fix_encoding(text):
    return fix_text(str(text)).strip() if pd.notna(text) else text

# %%
file_path = "2024_rankings.xlsx"

qs = pd.read_excel(file_path, sheet_name="qs")
the = pd.read_excel(file_path, sheet_name="the")

# %%
qs["University Name"] = qs["University Name"].apply(fix_encoding)
the["University Name"] = the["University Name"].apply(fix_encoding)
qs["Country"] = qs["Country"].apply(fix_encoding)
the["Country"] = the["Country"].apply(fix_encoding)

# %%
name_mapping = {
    # Switzerland
    "ETH Zurich - Swiss Federal Institute of Technology": "ETH Zurich",
    "EPFL": "École Polytechnique Fédérale de Lausanne",
    # Singapore
    "Nanyang Technological University, Singapore": "Nanyang Technological University",
    # Australia
    "The University of Melbourne": "University of Melbourne",
    "The University of Sydney": "University of Sydney",
    "The University of Queensland": "University of Queensland",
    "The University of Western Australia": "University of Western Australia",
    # Hong Kong
    "The University of Hong Kong": "University of Hong Kong",
    "The Chinese University of Hong Kong (CUHK)": "Chinese University of Hong Kong",
    "City University of Hong Kong": "City University of Hong Kong",
    "Hong Kong Polytechnic University": "The Hong Kong Polytechnic University",
    # Japan
    "The University of Tokyo": "University of Tokyo",
    "Kyoto University": "Kyoto University",
    # Korea
    "KAIST - Korea Advanced Institute of Science & Technology": "KAIST",
    "POSTECH": "Pohang University of Science and Technology",
    # China
    "Peking University": "Peking University",
    "Tsinghua University": "Tsinghua University",
    "Fudan University": "Fudan University",
    "Shanghai Jiao Tong University": "Shanghai Jiao Tong University",
    "Zhejiang University": "Zhejiang University",
    # United Kingdom
    "King's College London": "Kings College London",
    "The London School of Economics and Political Science (LSE)": "London School of Economics and Political Science",
    "The University of Warwick": "University of Warwick",
    "The University of Manchester": "University of Manchester",
    "The University of Edinburgh": "University of Edinburgh",
    "The University of Glasgow": "University of Glasgow",
    "The University of Sheffield": "University of Sheffield",
    "Queen Mary University of London": "Queen Mary University of London",
    # Germany
    "Ludwig-Maximilians-Universität München": "LMU Munich",
    "Technische Universität München": "Technical University of Munich",
    # Netherlands
    "Delft University of Technology": "Delft University of Technology",
    "Eindhoven University of Technology": "Eindhoven University of Technology",
    "University of Amsterdam": "University of Amsterdam",
    # Canada
    "University of Toronto": "University of Toronto",
    "McGill University": "McGill University",
    "University of British Columbia": "University of British Columbia",
    "University of Alberta": "University of Alberta",
    # USA
    "University of California, Berkeley (UCB)": "University of California Berkeley",
    "University of California, Los Angeles (UCLA)": "University of California Los Angeles",
    "University of California, San Diego (UCSD)": "University of California San Diego",
    "University of Illinois at Urbana-Champaign": "University of Illinois Urbana-Champaign",
    "Georgia Institute of Technology": "Georgia Institute of Technology",
    "Massachusetts Institute of Technology (MIT)": "Massachusetts Institute of Technology",
    "Carnegie Mellon University": "Carnegie Mellon University",
    # France
    "Université PSL": "PSL University",
    "Université Paris-Saclay": "Paris-Saclay University",
    # Belgium
    "KU Leuven": "Katholieke Universiteit Leuven",
    # Denmark
    "University of Copenhagen": "University of Copenhagen",
    "Technical University of Denmark": "Technical University of Denmark",
    # Sweden
    "KTH Royal Institute of Technology": "KTH Royal Institute of Technology",
    "Lund University": "Lund University",
    # Ireland
    "Trinity College Dublin, The University of Dublin": "Trinity College Dublin",
    # New Zealand
    "University of Auckland": "The University of Auckland",
    "Westfälische Wilhelms-Universität Münster": "University of Münster",
    "Rheinisch-Westfälische Technische Hochschule Aachen": "RWTH Aachen University",
    "Karlsruher Institut für Technologie": "Karlsruhe Institute of Technology",
    "Eberhard Karls Universität Tübingen": "University of Tübingen",
    "Georg-August-Universität Göttingen": "University of Göttingen",
    "Johannes Gutenberg-Universität Mainz": "Johannes Gutenberg University Mainz",
}
qs["University Name"] = qs["University Name"].replace(name_mapping)
the["University Name"] = the["University Name"].replace(name_mapping)

# %%
def clean_name(name):
    name = str(name)
    name = fix_encoding(name)
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r"[‐-‒–—−]", "-", name)
    name = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", name)
    name = re.sub(r"\s+", " ", name)
    # Remove accents
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("utf-8")
    name = name.lower()
    # Remove text inside brackets
    name = re.sub(r"\(.*?\)", "", name)
    translations = {
    "universidad": "university",
    "universite": "university",
    "universitat": "university",
    "universita": "university",
    "universiti": "university",
    "universidade": "university",
    "ecole": "school",
    "hochschule": "university",
    "technische": "technical",
    "technologico": "technology",
    "technologia": "technology",
    "federale": "federal",
    "federal": "federal",
    "nacional": "national",
    "nationale": "national",
    "autonoma": "autonomous",
    "autonome": "autonomous"
}
    for old, new in translations.items():
        name = name.replace(old, new)
    replacements = {
    "puc campinas": "pontificia universidade catolica do campinas",
    "unsw sydney": "university of new south wales",
    "skku": "sungkyunkwan university",
    "kaist": "korea advanced institute of science and technology",
    "postech": "pohang university of science and technology",
    "ntu": "national taiwan university",
    "mit": "massachusetts institute of technology",
    "epfl": "ecole polytechnique federale de lausanne",
    "psl": "paris sciences et lettres",
    "lse": "london school of economics and political science",
    "penn state": "pennsylvania state university",
    "ucb": "university of california berkeley",
    "ucla": "university of california los angeles",
    "ucsd": "university of california san diego"
}
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = re.sub(r"\b(de|del|da|do|of)\b", " ", name)
    replacements = {
    "â€“": "-",
    "–": "-",
    "—": "-",
    "â€”": "-",
    "â€™": "'",
    "’": "'",
    "Ã©": "e",
    "Ã¨": "e",
    "Ã¼": "u",
    "Ã¶": "o",
    "Ã¤": "a",
    "Ã±": "n",
    "Ã§": "c",
    "Ã¡": "a",
    "Ã³": "o",
    "Ãº": "u",
    "Ã": ""
}
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    remove_words = {
    "the",
    "of",
    "at",
    "for",
    "and",
    "campus",
    "campuses",
    "main",
    "college",
    "school",
    "faculty",
    "research",
    "center",
    "centre"
}
    words = [
        w
        for w in name.split()
        if w not in remove_words
    ]
    return " ".join(sorted(words))

# %%
qs["Merge_Name"] = qs["University Name"].apply(clean_name)
the["Merge_Name"] = the["University Name"].apply(clean_name)

# %%
auto_matches = {}
review_matches = []
for _, row in qs.iterrows():
    qs_name = row["Merge_Name"]
    qs_country = row["Country"]
    the_country = the[the["Country"] == qs_country]
    the_names = the_country["Merge_Name"].tolist()
    if len(the_names) == 0:
        continue
    match = process.extractOne(qs_name,the_names,scorer=fuzz.WRatio)
    if match:
        matched_name, score, _ = match
        if score >= 92:
            auto_matches[qs_name] = matched_name
        elif score >= 80:
            review_matches.append({
                "QS Name": qs_name,
                "Country": qs_country,
                "Suggested THE Name": matched_name,
                "Similarity": score
            })

# %%
qs["Merge_Name"] = qs["Merge_Name"].replace(auto_matches)
pd.DataFrame(review_matches).to_csv("review_matches.csv",index=False)
print("Auto Matches:", len(auto_matches))
print("Review Matches:", len(review_matches))

# %%
qs.drop_duplicates(subset="Merge_Name", inplace=True)
the.drop_duplicates(subset="Merge_Name", inplace=True)
qs.rename(columns={
    "World Rank": "QS Rank",
    "Overall Score": "QS Overall Score",
    "Citation Score": "QS Citation Score",
    "Academic Reputation Score": "Academic Reputation",
    "Employer Reputation Score": "Employer Reputation",
    "Faculty Student Score": "Faculty Student Score",
    "International Faculty Score": "International Faculty Score",
    "International Students Score": "International Students Score",
    "International Research Network Score": "International Research Network",
    "Employment Outcomes Score": "Employment Outcomes",
    "Sustainability Score": "Sustainability Score"
}, inplace=True)
the.rename(columns={
    "World Rank": "THE Rank",
    "Overall Score": "THE Overall Score",
    "Citation Score": "THE Citation Score",
    "scores_teaching": "Teaching Score",
    "scores_research": "Research Score",
    "scores_industry_income": "Industry Income",
    "scores_international_outlook": "International Outlook",
    "stats_number_students": "Number of Students",
    "stats_student_staff_ratio": "Student Staff Ratio",
    "stats_pc_intl_students": "International Students %",
    "stats_female_male_ratio": "Female Male Ratio"
}, inplace=True)

# %%
qs = qs[
[
"Merge_Name",
"University Name",
"Country",
"QS Rank",
"QS Overall Score",
"Academic Reputation",
"Employer Reputation",
"Faculty Student Score",
"QS Citation Score",
"International Faculty Score",
"International Students Score",
"International Research Network",
"Employment Outcomes",
"Sustainability Score"
]
]
the = the[
[
"Merge_Name",
"University Name",
"Country",
"THE Rank",
"THE Overall Score",
"Teaching Score",
"Research Score",
"THE Citation Score",
"Industry Income",
"International Outlook",
"Number of Students",
"Student Staff Ratio",
"International Students %"
]
]

# %%
merged = pd.merge(qs,the,on="Merge_Name",how="outer",suffixes=("_QS", "_THE"))
unmatched = merged[merged["QS Rank"].isna() |merged["THE Rank"].isna()]
unmatched.to_csv("unmatched_universities.csv",index=False)
print("Unmatched Universities:", unmatched.shape[0])

# %%
merged["University Name"] = merged["University Name_QS"].combine_first(merged["University Name_THE"])
merged["Country"] = merged["Country_QS"].combine_first(merged["Country_THE"])
merged.drop(columns=["Merge_Name","University Name_QS","University Name_THE","Country_QS","Country_THE"], inplace=True)

# %%
merged["QS Rank"] = (merged["QS Rank"].astype(str).str.replace("â€“", "-", regex=False).str.replace("–", "-", regex=False).str.strip())
merged["THE Rank"] = (merged["THE Rank"].astype(str).str.replace("â€“", "-", regex=False).str.replace("–", "-", regex=False).str.strip())
merged["Number of Students"] = (merged["Number of Students"].astype(str).str.replace(",", "", regex=False))
merged["Number of Students"] = pd.to_numeric(merged["Number of Students"],errors="coerce")
merged["Student Staff Ratio"] = pd.to_numeric(merged["Student Staff Ratio"],errors="coerce")

# %%
# Function to get the first number from a rank range
def rank_start(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    match = re.search(r"\d+", value)
    if match:
        return int(match.group())
    return None
merged["QS Rank Sort"] = merged["QS Rank"].apply(rank_start)
merged["THE Rank Sort"] = merged["THE Rank"].apply(rank_start)
merged["Sort Rank"] = (merged["QS Rank Sort"].combine_first(merged["THE Rank Sort"]))
merged.sort_values("Sort Rank", inplace=True)
merged.reset_index(drop=True, inplace=True)
merged.drop(columns=["QS Rank Sort", "THE Rank Sort", "Sort Rank"],inplace=True)

# %%
merged["THE Overall Score"] = (merged["THE Overall Score"].astype(str).str.replace("â€“", "-", regex=False).str.replace("–", "-", regex=False).str.strip())
merged["QS Overall Score"] = (merged["QS Overall Score"].astype(str).str.replace("â€“", "-", regex=False).str.replace("–", "-", regex=False).str.strip())

# %%
column_order = [
    "University Name",
    "Country",
    "THE Rank",
    "QS Rank",
    "THE Overall Score",
    "QS Overall Score",
    "Academic Reputation",
    "Employer Reputation",
    "Teaching Score",
    "Research Score",
    "THE Citation Score",
    "QS Citation Score",
    "Industry Income",
    "Faculty Student Score",
    "Student Staff Ratio",
    "Number of Students",
    "International Students %",
    "International Faculty Score",
    "International Students Score",
    "International Research Network",
    "International Outlook",
    "Employment Outcomes",
    "Sustainability Score"
]
merged = merged[column_order]
merged.to_csv("university_raw_data.csv", index=False)
print("=" * 60)
print("Merged Successfully")
print("Rows :", merged.shape[0])
print("Columns :", merged.shape[1])
print("\nMissing Values (%)")
print((merged.isnull().mean() * 100).round(2))
print("=" * 60)