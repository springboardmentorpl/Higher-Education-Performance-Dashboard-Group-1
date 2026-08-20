# ============================================================
# EDUVISION DV - MODERN DASHBOARD STORYBOARD PDF
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# ============================================================
# PATHS
# ============================================================

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT = os.path.join(
    BASE, "data", "final", "university_final_dataset.xlsx"
)

OUT = os.path.join(
    BASE, "data", "visualizations"
)

PDF = os.path.join(
    OUT, "dashboard_storyboard.pdf"
)

os.makedirs(OUT, exist_ok=True)


# ============================================================
# THEME
# ============================================================

NAVY = "#090B20"
PURPLE = "#7C3AED"
VIOLET = "#A855F7"
CYAN = "#22D3EE"
PINK = "#EC4899"
TEXT = "#F8FAFC"
MUTED = "#A5B4FC"
CARD = "#151936"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading EduVision dataset...")

df = pd.read_excel(INPUT)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# CHART HELPER
# ============================================================

def chart(name, kind, title, data=None, x=None, y=None):

    plt.figure(figsize=(6, 3.1))
    ax = plt.gca()
    ax.set_facecolor(NAVY)
    plt.gcf().patch.set_facecolor(NAVY)

    if kind == "bar":
        data.plot(
            kind="barh",
            color=PURPLE,
            ax=ax
        )

    elif kind == "pie":
        ax.pie(
            data.values,
            labels=data.index,
            autopct="%1.0f%%",
            startangle=90,
            wedgeprops={"width": 0.42},
            textprops={"color": TEXT, "fontsize": 7}
        )

    elif kind == "hist":
        ax.hist(
            data.dropna(),
            bins=12,
            color=VIOLET,
            alpha=.85
        )

    elif kind == "line":
        ax.plot(
            data.index,
            data.values,
            color=CYAN,
            linewidth=2.5,
            marker="o",
            markersize=3
        )

    elif kind == "scatter":
        ax.scatter(
            x,
            y,
            color=CYAN,
            alpha=.65,
            s=18
        )

    elif kind == "bubble":
        sizes = np.nan_to_num(
            data["size"].values * 4,
            nan=20
        )

        ax.scatter(
            data["x"],
            data["y"],
            s=sizes,
            color=VIOLET,
            alpha=.55,
            edgecolors=CYAN
        )

    ax.set_title(
        title,
        color=TEXT,
        fontsize=10,
        fontweight="bold",
        pad=10
    )

    ax.tick_params(
        colors=MUTED,
        labelsize=6
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(
        alpha=.08,
        color="white"
    )

    plt.tight_layout()

    path = os.path.join(OUT, name)
    plt.savefig(
        path,
        dpi=160,
        facecolor=NAVY,
        bbox_inches="tight"
    )

    plt.close()

    return path


# ============================================================
# PREPARE DATA
# ============================================================

top = (
    df.nlargest(
        10,
        "KPI_Global_Ranking_Score"
    )
    .set_index("Institution_Name")
    ["KPI_Global_Ranking_Score"]
)

regions = (
    df["Region"]
    .value_counts()
    .head(6)
)

score = df["KPI_Global_Ranking_Score"]

research = (
    df.nlargest(
        10,
        "KPI_Research_Impact_Score"
    )
    .set_index("Institution_Name")
    ["KPI_Research_Impact_Score"]
)

research_line = (
    df.groupby("Rank_2026")
    ["KPI_Research_Impact_Score"]
    .mean()
    .dropna()
    .sort_index()
    .head(15)
)

students = (
    df.nlargest(
        10,
        "KPI_International_Student_Percentage"
    )
    .set_index("Institution_Name")
    ["KPI_International_Student_Percentage"]
)

countries = (
    df.groupby("Country")
    ["KPI_Global_Ranking_Score"]
    .mean()
    .nlargest(10)
)

country_size = (
    df.groupby("Country")
    .agg(
        x=("KPI_Global_Ranking_Score", "mean"),
        y=("KPI_Research_Impact_Score", "mean"),
        size=("Institution_Name", "count")
    )
    .dropna()
    .nlargest(12, "size")
)


# ============================================================
# CREATE CHARTS
# ============================================================

print("Creating dashboard charts...")

C = {}

# Overview
C["top"] = chart(
    "overview_bar.png",
    "bar",
    "Top Universities by Global Score",
    top
)

C["region"] = chart(
    "overview_pie.png",
    "pie",
    "University Distribution by Region",
    regions
)

C["hist"] = chart(
    "overview_hist.png",
    "hist",
    "Global Score Distribution",
    score
)

C["line"] = chart(
    "overview_line.png",
    "line",
    "Research Trend by Ranking",
    research_line
)

# Research
C["research"] = chart(
    "research_bar.png",
    "bar",
    "Research Impact Leaders",
    research
)

C["research_scatter"] = chart(
    "research_scatter.png",
    "scatter",
    "Research Impact vs Academic Reputation",
    x=df["KPI_Research_Impact_Score"],
    y=df["KPI_Academic_Reputation_Score"]
)

C["research_bubble"] = chart(
    "research_bubble.png",
    "bubble",
    "Research Impact Bubble Analysis",
    data=pd.DataFrame({
        "x": df["KPI_Research_Impact_Score"],
        "y": df["KPI_Research_Productivity_Index"],
        "size": df["KPI_Global_Ranking_Score"]
    }).dropna()
)

C["research_line"] = chart(
    "research_line.png",
    "line",
    "Research Productivity Trend",
    df["KPI_Research_Productivity_Index"]
    .dropna()
    .head(20)
    .reset_index(drop=True)
)

# Students
C["student_bar"] = chart(
    "student_bar.png",
    "bar",
    "International Student Leaders",
    students
)

C["student_pie"] = chart(
    "student_pie.png",
    "pie",
    "Regional Student Distribution",
    regions
)

C["student_hist"] = chart(
    "student_hist.png",
    "hist",
    "International Student Distribution",
    df["KPI_International_Student_Percentage"]
)

C["student_scatter"] = chart(
    "student_scatter.png",
    "scatter",
    "Faculty Ratio vs International Students",
    x=df["KPI_Faculty_to_Student_Ratio"],
    y=df["KPI_International_Student_Percentage"]
)

# Country
C["country_bar"] = chart(
    "country_bar.png",
    "bar",
    "Top Countries by Average Score",
    countries
)

C["country_pie"] = chart(
    "country_pie.png",
    "pie",
    "Universities by Region",
    regions
)

C["country_bubble"] = chart(
    "country_bubble.png",
    "bubble",
    "Country Performance Bubble Map",
    country_size
)

C["country_line"] = chart(
    "country_line.png",
    "line",
    "Country Score Comparison",
    countries.sort_values()
)


# ============================================================
# PDF STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontSize=20,
    textColor=colors.white
)

small = ParagraphStyle(
    "Small",
    parent=styles["Normal"],
    fontSize=7,
    textColor=colors.HexColor(MUTED)
)

kpi_style = ParagraphStyle(
    "KPI",
    parent=styles["Normal"],
    fontSize=14,
    alignment=TA_CENTER,
    textColor=colors.white
)


# ============================================================
# HEADER
# ============================================================

def header(title):

    t = Table([[
        Paragraph(
            f"<b>EDUVISION DV</b><br/>{title}",
            title_style
        ),
        Paragraph(
            "HIGHER EDUCATION<br/>PERFORMANCE ANALYTICS",
            small
        )
    ]], colWidths=[7.8 * inch, 2.5 * inch])

    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(NAVY)),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE")
    ]))

    return t


# ============================================================
# NAVIGATION
# ============================================================

def navigation(active):

    pages = [
        "OVERVIEW",
        "RESEARCH",
        "STUDENTS",
        "COUNTRIES"
    ]

    cells = []

    for p in pages:

        color = (
            colors.white
            if p == active
            else colors.HexColor(MUTED)
        )

        cells.append(
            Paragraph(
                f"<b>{p}</b>",
                ParagraphStyle(
                    "Nav",
                    parent=small,
                    alignment=TA_CENTER,
                    textColor=color
                )
            )
        )

    t = Table(
        [cells],
        colWidths=[2.575 * inch] * 4
    )

    commands = [
        (
            "BACKGROUND",
            (0,0),
            (-1,-1),
            colors.HexColor(CARD)
        ),
        (
            "TOPPADDING",
            (0,0),
            (-1,-1),
            7
        ),
        (
            "BOTTOMPADDING",
            (0,0),
            (-1,-1),
            7
        )
    ]

    index = pages.index(active)

    commands.append(
        (
            "BACKGROUND",
            (index,0),
            (index,0),
            colors.HexColor(PURPLE)
        )
    )

    t.setStyle(TableStyle(commands))

    return t


# ============================================================
# KPI CARD
# ============================================================

def kpi(label, value):

    t = Table([[
        Paragraph(
            f"<b>{value}</b><br/><font size=6>{label}</font>",
            kpi_style
        )
    ]], colWidths=[2.45 * inch], rowHeights=[.62 * inch])

    t.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0,0),
            (-1,-1),
            colors.HexColor(CARD)
        ),
        (
            "BOX",
            (0,0),
            (-1,-1),
            1,
            colors.HexColor(PURPLE)
        ),
        (
            "VALIGN",
            (0,0),
            (-1,-1),
            "MIDDLE"
        )
    ]))

    return t


# ============================================================
# FILTER PANEL
# ============================================================

def filters():

    rows = [
        ["FILTERS"],
        ["Country   ▾"],
        ["Region   ▾"],
        ["University   ▾"],
        ["Rank Range   ▾"],
        ["Reset Filters"]
    ]

    t = Table(
        [[Paragraph(f"<b>{x}</b>", small)] for x in rows],
        colWidths=[1.65 * inch]
    )

    t.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0,0),
            (-1,0),
            colors.HexColor(PURPLE)
        ),
        (
            "BACKGROUND",
            (0,1),
            (-1,-1),
            colors.HexColor(CARD)
        ),
        (
            "BOX",
            (0,0),
            (-1,-1),
            .8,
            colors.HexColor(VIOLET)
        ),
        (
            "LINEBELOW",
            (0,0),
            (-1,-2),
            .3,
            colors.HexColor("#30345A")
        ),
        (
            "LEFTPADDING",
            (0,0),
            (-1,-1),
            8
        ),
        (
            "TOPPADDING",
            (0,0),
            (-1,-1),
            7
        ),
        (
            "BOTTOMPADDING",
            (0,0),
            (-1,-1),
            7
        )
    ]))

    return t


# ============================================================
# PAGE BUILDER
# ============================================================

def build_page(
    active,
    charts,
    values
):

    story.append(header(active))
    story.append(Spacer(1,5))
    story.append(navigation(active))
    story.append(Spacer(1,7))

    story.append(
        Table(
            [[kpi(a,b) for a,b in values]],
            colWidths=[2.575 * inch] * 4
        )
    )

    story.append(Spacer(1,8))

    top = Table([[
        filters(),
        Image(
            charts[0],
            width=3.75 * inch,
            height=2.25 * inch
        ),
        Image(
            charts[1],
            width=3.75 * inch,
            height=2.25 * inch
        )
    ]], colWidths=[
        1.8 * inch,
        4.15 * inch,
        4.15 * inch
    ])

    top.setStyle(TableStyle([
        (
            "VALIGN",
            (0,0),
            (-1,-1),
            "TOP"
        ),
        (
            "LEFTPADDING",
            (0,0),
            (-1,-1),
            3
        ),
        (
            "RIGHTPADDING",
            (0,0),
            (-1,-1),
            3
        )
    ]))

    story.append(top)
    story.append(Spacer(1,6))

    bottom = Table([[
        Image(
            charts[2],
            width=4.9 * inch,
            height=2.35 * inch
        ),
        Image(
            charts[3],
            width=4.9 * inch,
            height=2.35 * inch
        )
    ]], colWidths=[
        5.15 * inch,
        5.15 * inch
    ])

    bottom.setStyle(TableStyle([
        (
            "VALIGN",
            (0,0),
            (-1,-1),
            "TOP"
        )
    ]))

    story.append(bottom)


# ============================================================
# BUILD PDF
# ============================================================

print("Building modern dashboard PDF...")

doc = SimpleDocTemplate(
    PDF,
    pagesize=landscape(A4),
    leftMargin=18,
    rightMargin=18,
    topMargin=18,
    bottomMargin=18
)

story = []


# PAGE 1
build_page(
    "OVERVIEW",
    [
        C["top"],
        C["region"],
        C["hist"],
        C["line"]
    ],
    [
        ("UNIVERSITIES", f"{len(df):,}"),
        ("COUNTRIES", f"{df.Country.nunique():,}"),
        ("GLOBAL SCORE", f"{df.KPI_Global_Ranking_Score.mean():.2f}"),
        ("RESEARCH IMPACT", f"{df.KPI_Research_Impact_Score.mean():.2f}")
    ]
)

story.append(PageBreak())


# PAGE 2
build_page(
    "RESEARCH",
    [
        C["research"],
        C["research_scatter"],
        C["research_bubble"],
        C["research_line"]
    ],
    [
        ("RESEARCH IMPACT", f"{df.KPI_Research_Impact_Score.mean():.2f}"),
        ("PRODUCTIVITY", f"{df.KPI_Research_Productivity_Index.mean():.2f}"),
        ("ACADEMIC REPUTATION", f"{df.KPI_Academic_Reputation_Score.mean():.2f}"),
        ("CITATIONS", f"{df.Citations_per_Faculty_Score.mean():.2f}")
    ]
)

story.append(PageBreak())


# PAGE 3
build_page(
    "STUDENTS",
    [
        C["student_bar"],
        C["student_pie"],
        C["student_hist"],
        C["student_scatter"]
    ],
    [
        ("INTL. STUDENTS", f"{df.KPI_International_Student_Percentage.mean():.2f}%"),
        ("FACULTY / STUDENT", f"{df.KPI_Faculty_to_Student_Ratio.mean():.2f}"),
        ("INTL. FACULTY", f"{df.International_Faculty_Score.mean():.2f}"),
        ("UNIVERSITIES", f"{len(df):,}")
    ]
)

story.append(PageBreak())


# PAGE 4
build_page(
    "COUNTRIES",
    [
        C["country_bar"],
        C["country_pie"],
        C["country_bubble"],
        C["country_line"]
    ],
    [
        ("COUNTRIES", f"{df.Country.nunique():,}"),
        ("UNIVERSITIES", f"{len(df):,}"),
        ("AVG SCORE", f"{df.KPI_Global_Ranking_Score.mean():.2f}"),
        ("AVG RESEARCH", f"{df.KPI_Research_Impact_Score.mean():.2f}")
    ]
)


doc.build(story)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("EDUVISION MODERN DASHBOARD COMPLETE")
print("=" * 60)
print("PDF:", PDF)
print("Charts: Bar | Pie/Donut | Histogram | Line | Scatter | Bubble")
print("Theme: Dark Navy | Purple | Violet | Cyan")
print("Filters: Fixed")
print("STATUS: SUCCESS")
print("=" * 60)