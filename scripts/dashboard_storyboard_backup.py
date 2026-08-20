# ============================================================
# EDUVISION - MODULE 4 DASHBOARD STORYBOARD
# University Overview | Research Analytics
# Student Analytics | Country Comparison
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "final",
    "university_final_dataset.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "visualizations"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "dashboard_storyboard.pdf"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("Loading final university dataset...")

df = pd.read_excel(INPUT_FILE)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def numeric_column(name):
    if name in df.columns:
        return pd.to_numeric(df[name], errors="coerce")
    return pd.Series([0] * len(df))


def save_chart(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


# ============================================================
# 4. CREATE CHARTS FROM REAL DATA
# ============================================================

print("Creating dashboard charts...")


# ---------- University Overview ----------
top_universities = (
    df.sort_values("KPI_Global_Ranking_Score", ascending=False)
      .head(10)
      .sort_values("KPI_Global_Ranking_Score")
)

plt.figure(figsize=(7, 4))
plt.barh(
    top_universities["Institution_Name"],
    top_universities["KPI_Global_Ranking_Score"]
)
plt.xlabel("Global Ranking Score")
plt.title("Top 10 Universities")
plt.grid(axis="x", alpha=0.25)
overview_chart = save_chart("module4_top_universities.png")


# ---------- Research Analytics ----------
research = (
    df.sort_values("KPI_Research_Impact_Score", ascending=False)
      .head(10)
      .sort_values("KPI_Research_Impact_Score")
)

plt.figure(figsize=(7, 4))
plt.barh(
    research["Institution_Name"],
    research["KPI_Research_Impact_Score"]
)
plt.xlabel("Research Impact Score")
plt.title("Top Research Institutions")
plt.grid(axis="x", alpha=0.25)
research_chart = save_chart("module4_research_impact.png")


# ---------- Student Analytics ----------
student = (
    df.sort_values(
        "KPI_International_Student_Percentage",
        ascending=False
    )
    .head(10)
    .sort_values("KPI_International_Student_Percentage")
)

plt.figure(figsize=(7, 4))
plt.barh(
    student["Institution_Name"],
    student["KPI_International_Student_Percentage"]
)
plt.xlabel("International Student Percentage")
plt.title("International Student Distribution")
plt.grid(axis="x", alpha=0.25)
student_chart = save_chart("module4_student_analytics.png")


# ---------- Country Comparison ----------
country_data = (
    df.groupby("Country")
      .agg(
          Universities=("Institution_Name", "count"),
          Average_Score=("KPI_Global_Ranking_Score", "mean")
      )
      .sort_values("Average_Score", ascending=False)
      .head(10)
      .sort_values("Average_Score")
)

plt.figure(figsize=(7, 4))
plt.barh(
    country_data.index,
    country_data["Average_Score"]
)
plt.xlabel("Average Global Ranking Score")
plt.title("Top Countries by Average Score")
plt.grid(axis="x", alpha=0.25)
country_chart = save_chart("module4_country_comparison.png")


# ============================================================
# 5. PDF STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "DashboardTitle",
    parent=styles["Title"],
    fontSize=24,
    leading=28,
    textColor=colors.white,
    spaceAfter=10
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=9,
    textColor=colors.white
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontSize=15,
    leading=18,
    textColor=colors.HexColor("#172A46"),
    spaceAfter=8
)

normal_style = ParagraphStyle(
    "NormalCustom",
    parent=styles["Normal"],
    fontSize=9,
    leading=13
)

small_style = ParagraphStyle(
    "Small",
    parent=styles["Normal"],
    fontSize=7,
    leading=9
)


# ============================================================
# 6. DASHBOARD HEADER
# ============================================================

def dashboard_header(title, subtitle):

    data = [[
        Paragraph(
            f"<b>EduVision DV</b><br/>{title}",
            title_style
        ),
        Paragraph(
            f"MODULE 4<br/>{subtitle}",
            subtitle_style
        )
    ]]

    table = Table(data, colWidths=[7.2 * inch, 2.2 * inch])

    table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            colors.HexColor("#172A46")
        ),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))

    return table


# ============================================================
# 7. NAVIGATION BAR
# ============================================================

def navigation_bar(active):

    pages = [
        "University Overview",
        "Research Analytics",
        "Student Analytics",
        "Country Comparison"
    ]

    row = []

    for page in pages:

        if page == active:
            bg = colors.HexColor("#7652B3")
            text = colors.white
        else:
            bg = colors.HexColor("#E7EDF3")
            text = colors.HexColor("#172A46")

        row.append(
            Paragraph(
                f"<b>{page}</b>",
                ParagraphStyle(
                    "Nav",
                    parent=small_style,
                    alignment=TA_CENTER,
                    textColor=text
                )
            )
        )

    table = Table(
        [row],
        colWidths=[2.25 * inch] * 4
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#E7EDF3")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E7EDF3")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#E7EDF3")),
        ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#E7EDF3")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.white),
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    # Highlight active tab
    active_index = pages.index(active)

    table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (active_index, 0),
            (active_index, 0),
            colors.HexColor("#7652B3")
        )
    ]))

    return table


# ============================================================
# 8. FILTER PANEL
# ============================================================

def filter_panel():

    filters = [
        ["FILTERS", "Navigation / Dashboard Actions"],
        ["Country", "Select country"],
        ["Region", "Select region"],
        ["University", "Select university"],
        ["Rank Range", "Select ranking range"],
        ["Reset Filters", "Compare / Drill-down"]
    ]

    table = Table(
        filters,
        colWidths=[1.5 * inch, 2.5 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172A46")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F5F8")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DDE5")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    return table


# ============================================================
# 9. KPI CARDS
# ============================================================

def kpi_cards():

    cards = [
        ["UNIVERSITIES", f"{len(df):,}"],
        [
            "AVG GLOBAL SCORE",
            f"{df['KPI_Global_Ranking_Score'].mean():.2f}"
        ],
        [
            "AVG RESEARCH IMPACT",
            f"{df['KPI_Research_Impact_Score'].mean():.2f}"
        ],
        [
            "AVG INTL. STUDENTS",
            f"{df['KPI_International_Student_Percentage'].mean():.2f}%"
        ]
    ]

    table = Table(
        [
            [
                Paragraph(
                    f"<b>{x[0]}</b><br/><font size=16>{x[1]}</font>",
                    small_style
                )
                for x in cards
            ]
        ],
        colWidths=[2.15 * inch] * 4
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DDE5")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DDE5")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    return table


# ============================================================
# 10. BUILD PDF
# ============================================================

print("Building dashboard storyboard PDF...")

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=landscape(A4),
    rightMargin=25,
    leftMargin=25,
    topMargin=25,
    bottomMargin=25
)

story = []


# ============================================================
# PAGE 1 - UNIVERSITY OVERVIEW
# ============================================================

story.append(
    dashboard_header(
        "University Overview",
        "University performance overview"
    )
)

story.append(Spacer(1, 10))
story.append(navigation_bar("University Overview"))
story.append(Spacer(1, 10))
story.append(kpi_cards())
story.append(Spacer(1, 12))

layout1 = Table([
    [
        filter_panel(),
        Image(overview_chart, width=6.2 * inch, height=3.5 * inch)
    ]
], colWidths=[4.1 * inch, 6.3 * inch])

layout1.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP")
]))

story.append(layout1)
story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Dashboard actions:</b> Select a university to drill down into its "
        "ranking, reputation, research and international indicators. "
        "Filters update the displayed comparison.",
        normal_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 2 - RESEARCH ANALYTICS
# ============================================================

story.append(
    dashboard_header(
        "Research Analytics",
        "Research performance and impact"
    )
)

story.append(Spacer(1, 10))
story.append(navigation_bar("Research Analytics"))
story.append(Spacer(1, 10))

research_kpis = Table([
    [
        "Research Impact",
        f"{df['KPI_Research_Impact_Score'].mean():.2f}",
        "Research Productivity",
        f"{df['KPI_Research_Productivity_Index'].mean():.2f}",
        "Academic Reputation",
        f"{df['KPI_Academic_Reputation_Score'].mean():.2f}"
    ]
], colWidths=[1.5 * inch, 1.2 * inch] * 3)

research_kpis.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DDE5")),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))

story.append(research_kpis)
story.append(Spacer(1, 15))

layout2 = Table([
    [
        Image(research_chart, width=6.5 * inch, height=3.7 * inch),
        filter_panel()
    ]
], colWidths=[6.7 * inch, 3.7 * inch])

layout2.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP")
]))

story.append(layout2)
story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "<b>Interactive comparison:</b> Compare institutions using research "
        "impact, productivity and academic reputation. Selecting a country "
        "or university filters the research view.",
        normal_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 3 - STUDENT ANALYTICS
# ============================================================

story.append(
    dashboard_header(
        "Student Analytics",
        "International students and student distribution"
    )
)

story.append(Spacer(1, 10))
story.append(navigation_bar("Student Analytics"))
story.append(Spacer(1, 10))
story.append(kpi_cards())
story.append(Spacer(1, 12))

layout3 = Table([
    [
        filter_panel(),
        Image(student_chart, width=6.2 * inch, height=3.5 * inch)
    ]
], colWidths=[4.1 * inch, 6.3 * inch])

layout3.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP")
]))

story.append(layout3)
story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Student filters:</b> Country, region and university can be used "
        "to compare international student percentage and faculty-to-student "
        "ratio. Dashboard selections should update all related visuals.",
        normal_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 4 - COUNTRY COMPARISON
# ============================================================

story.append(
    dashboard_header(
        "Country Comparison",
        "Compare higher-education performance by country"
    )
)

story.append(Spacer(1, 10))
story.append(navigation_bar("Country Comparison"))
story.append(Spacer(1, 10))

country_kpis = Table([
    [
        "Countries",
        f"{df['Country'].nunique():,}",
        "Universities",
        f"{len(df):,}",
        "Overall Average",
        f"{df['KPI_Global_Ranking_Score'].mean():.2f}"
    ]
], colWidths=[1.5 * inch, 1.2 * inch] * 3)

country_kpis.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DDE5")),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))

story.append(country_kpis)
story.append(Spacer(1, 12))

layout4 = Table([
    [
        Image(country_chart, width=6.5 * inch, height=3.7 * inch),
        filter_panel()
    ]
], colWidths=[6.7 * inch, 3.7 * inch])

layout4.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP")
]))

story.append(layout4)
story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Country comparison action:</b> Selecting a country filters the "
        "university list and allows comparison of average global ranking "
        "score, research impact and international student performance.",
        normal_style
    )
)


# ============================================================
# 11. BUILD
# ============================================================

doc.build(story)

print()
print("============================================================")
print("MODULE 4 DASHBOARD STORYBOARD COMPLETE")
print("============================================================")
print("PDF created:")
print(OUTPUT_FILE)
print()
print("Pages:")
print("1. University Overview")
print("2. Research Analytics")
print("3. Student Analytics")
print("4. Country Comparison")
print()
print("Features represented:")
print("- Navigation")
print("- Filters")
print("- Dashboard actions")
print("- Interactive comparisons")
print("- KPI cards")
print("- Real dataset charts")
print("============================================================")