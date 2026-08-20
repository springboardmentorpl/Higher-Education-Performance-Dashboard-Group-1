import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION DV - INTERACTIVE DASHBOARD
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "final" / "university_final_dataset.xlsx"

st.set_page_config(
    page_title="EduVision DV",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#080816,#120B25,#08172B);
    color: white;
}

[data-testid="stSidebar"] {
    background: #0B0820;
}

h1 {
    color:#D8B4FE !important;
}

h2,h3 {
    color:#BFA2FF !important;
}

.kpi {
    background: linear-gradient(135deg,#241344,#142A4D);
    border:1px solid #7048B8;
    border-radius:18px;
    padding:18px;
    text-align:center;
    box-shadow:0 0 18px rgba(126,87,194,.18);
}

.kpi-title {
    color:#B9A5D8;
    font-size:13px;
}

.kpi-value {
    color:white;
    font-size:27px;
    font-weight:bold;
}

.block {
    background:rgba(25,18,48,.72);
    border:1px solid #3F2B68;
    border-radius:18px;
    padding:18px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_excel(DATA_FILE)

df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🎓 EduVision DV")
st.sidebar.caption("Higher Education Performance Analytics")

countries = sorted(
    df["Country"].dropna().unique()
)

country = st.sidebar.selectbox(
    "🌍 Country",
    ["All Countries"] + countries
)

regions = sorted(
    df["Region"].dropna().unique()
)

region = st.sidebar.selectbox(
    "📍 Region",
    ["All Regions"] + regions
)

data = df.copy()

if country != "All Countries":
    data = data[data["Country"] == country]

if region != "All Regions":
    data = data[data["Region"] == region]

st.sidebar.markdown("---")
st.sidebar.caption("Filters update all dashboard analytics.")

# ============================================================
# HEADER
# ============================================================

st.title("🎓 EduVision DV")
st.markdown("### University Performance Dashboard")
st.caption(
    "Explore global rankings, research impact, reputation "
    "and internationalization."
)

# ============================================================
# KPI CARDS
# ============================================================

c1,c2,c3,c4 = st.columns(4)

def card(col,title,value):
    with col:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

card(
    c1,
    "🏫 UNIVERSITIES",
    f"{len(data):,}"
)

card(
    c2,
    "🌍 COUNTRIES",
    f"{data['Country'].nunique():,}"
)

card(
    c3,
    "🏆 GLOBAL SCORE",
    f"{data['KPI_Global_Ranking_Score'].mean():.2f}"
)

card(
    c4,
    "🔬 RESEARCH IMPACT",
    f"{data['KPI_Research_Impact_Score'].mean():.2f}"
)

st.write("")

# ============================================================
# TOP UNIVERSITIES
# ============================================================

left,right = st.columns(2)

with left:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("🏆 Top Universities")

    top = (
        data.nlargest(
            10,
            "KPI_Global_Ranking_Score"
        )
        [["Institution_Name",
          "KPI_Global_Ranking_Score"]]
        .set_index("Institution_Name")
    )

    st.bar_chart(
        top,
        height=330
    )

    st.markdown("</div>", unsafe_allow_html=True)


with right:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("🌍 Universities by Country")

    country_count = (
        data.groupby("Country")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        country_count,
        height=330
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RESEARCH + REPUTATION
# ============================================================

st.write("")

a,b = st.columns(2)

with a:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("🔬 Research Analytics")

    research = (
        data.nlargest(
            10,
            "KPI_Research_Impact_Score"
        )
        [["Institution_Name",
          "KPI_Research_Impact_Score"]]
        .set_index("Institution_Name")
    )

    st.bar_chart(
        research,
        height=320
    )

    st.markdown("</div>", unsafe_allow_html=True)


with b:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("🎯 Reputation Analysis")

    reputation = (
        data[
            [
                "Institution_Name",
                "KPI_Academic_Reputation_Score",
                "Employer_Reputation_Score"
            ]
        ]
        .dropna()
        .head(10)
        .set_index("Institution_Name")
    )

    st.bar_chart(
        reputation,
        height=320
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# INTERNATIONALIZATION
# ============================================================

st.write("")

a,b = st.columns(2)

with a:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("🌐 International Students")

    intl_students = (
        data.nlargest(
            10,
            "KPI_International_Student_Percentage"
        )
        [["Institution_Name",
          "KPI_International_Student_Percentage"]]
        .set_index("Institution_Name")
    )

    st.bar_chart(
        intl_students,
        height=320
    )

    st.markdown("</div>", unsafe_allow_html=True)


with b:

    st.markdown(
        '<div class="block">',
        unsafe_allow_html=True
    )

    st.subheader("👨‍🏫 Faculty / Student KPI")

    ratio = (
        data.nlargest(
            10,
            "KPI_Faculty_to_Student_Ratio"
        )
        [["Institution_Name",
          "KPI_Faculty_to_Student_Ratio"]]
        .set_index("Institution_Name")
    )

    st.bar_chart(
        ratio,
        height=320
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# UNIVERSITY SEARCH
# ============================================================

st.write("")

st.subheader("🔎 University Search")

search = st.text_input(
    "Search university name"
)

if search:

    result = data[
        data["Institution_Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if not result.empty:

        st.dataframe(
            result[
                [
                    "Institution_Name",
                    "Country",
                    "Region",
                    "Current_Rank",
                    "KPI_Global_Ranking_Score",
                    "KPI_Research_Impact_Score",
                    "KPI_Academic_Reputation_Score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No university found."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "EduVision DV • Higher Education Performance Analytics • "
    "Module 4 Dashboard"
)