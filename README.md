# Higher-Education-Performance-Dashboard-Group-1
Project Repository for Higher Education Performance Dashboard - Group 1
# 🎓 EduVision_DV — Higher Education Performance Dashboard

From fragmented university-ranking data to an interactive global higher-education analytics experience.

---

## 📌 Project Overview

**EduVision_DV** is an end-to-end Data Visualization project developed as part of the **Infosys Springboard 7.0 Data Visualization Internship**. 

The project integrates data from the **2024 QS World University Rankings** and **2024 Times Higher Education (THE) World University Rankings**, followed by extensive data cleaning, transformation, integration, and KPI development. The processed data is presented through a suite of **four interactive Tableau dashboards**, providing complementary perspectives on university performance, research, students, and country-level education trends.

The project focuses not only on creating visualizations, but on building a structured analytical workflow that transforms complex and inconsistent higher-education data into a clear, interactive, and visually consistent decision-support experience.

---

## 🎯 Project Objective

Higher-education ranking datasets contain a large number of academic, research, student, institutional, and geographical metrics. However, these datasets come from different sources and often contain inconsistent structures, missing values, and redundant information.

The objective of EduVision_DV is to:
* Integrate QS and THE university-ranking datasets
* Clean and transform fragmented higher-education data
* Reduce unnecessary and redundant fields
* Prepare a structured analytical dataset
* Develop meaningful education-focused KPIs
* Create interactive and synchronized dashboards
* Enable university, research, student, and country-level comparisons
* Present complex data through an intuitive and consistent UI/UX

---

## 🔎 Analytical Perspectives

The final dashboard suite provides four complementary perspectives:

1. **University Overview**
2. **Research Analytics**
3. **Student Analytics**
4. **Country Comparison**

---

## 🔄 End-to-End Project Workflow

```text
QS World University Rankings 2024
                 +
Times Higher Education Rankings 2024
                 │
                 ▼
     Data Collection & Integration
                 │
                 ▼
     Initial Integrated Dataset
     ~3,466 Rows / ~55 Columns
                 │
                 ▼
    Data Cleaning & Transformation
                 │
                 ▼
    Feature Selection & Preparation
                 │
                 ▼
          620 Universities
                 │
                 ▼
          KPI Engineering
                 │
                 ▼
     Final Analytical Dataset
                 │
                 ▼
      Tableau Dashboard Development
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼         ▼
   University  Research  Student   Country
    Overview   Analytics Analytics Comparison

📊 Data SourcesThe project uses two major global university-ranking datasets:1. QS World University Rankings 2024The QS dataset contains indicators related to areas such as:Academic ReputationEmployer ReputationFaculty-to-Student RatioCitations per FacultyInternational FacultySustainabilityOverall University Score2. Times Higher Education (THE) World University Rankings 2024The THE dataset provides additional indicators covering areas such as:TeachingResearchCitationsInternational OutlookStudent-related metricsInstitutional performance🔗 Data IntegrationThe two datasets were integrated using an outer join to combine information from both ranking sources and preserve relevant university records.Initial merged dataset: ~3,466 rows / ~55 columnsFinal analytical dataset (post-cleaning): 620 universities / 44 relevant analytical columns🧹 Data Cleaning & TransformationData preparation was one of the major stages of the project. The raw datasets contained missing values, unnecessary fields, inconsistent structures, and overlapping information.Key Data Preparation StepsDataset inspection and profilingHandling missing valuesRemoving unnecessary columns and redundant fieldsStandardizing relevant fieldsIntegrating QS and THE datasetsSelecting meaningful analytical attributesValidating and preparing the final dataset for visualization📐 KPI EngineeringTo convert raw ranking indicators into meaningful dashboard-level insights, education-focused KPIs were developed across the four analytical modules, covering:Overall university performance & academic/employer reputationResearch impact, citations, and international research representationStudent demographics, faculty-to-student ratios, and international outlookCountry-level university performance summaries🚀 Dashboard Modules1. 🏫 University OverviewFocus: High-level view of global university performance, institutional reputation, and geographical distribution.Key Visualizations: Top Global University Rankings, Top 10 Universities by Employer Reputation, University Distribution by Country, Global University Distribution Map.KPIs: Total Universities, Average Overall Score, Average Academic Reputation, Average Employer Reputation.2. 🔬 Research AnalyticsFocus: Analyzes research performance, academic output, and the global research footprint of universities.Key Visualizations: Publications Analysis, Top Research Institutions, Custom Packed Bubble Chart, Research Productivity Trends, Research Productivity Scatter Plot.KPIs: Average Research Impact, Average Citations per Student, Average International Research Network, Average Research Productivity.3. 👨‍🎓 Student AnalyticsFocus: Examines student demographics, international representation, enrollment, and student-related institutional metrics.Key Visualizations: International Student Analysis, Student Distribution Map, Student Enrollment Comparisons, International Student Distribution.KPIs: Average International Students, Average Female Students %, Average Faculty Ratio, Total Students Enrolled.4. 🌍 Country ComparisonFocus: Macro-level comparison of higher-education performance across countries.Key Visualizations: Top Performing Countries, International Outlook Spread, International Outlook Box Plot, Top 5 Student Populations, Student Population Pie Chart.KPIs: Total Countries, Average Global Score, Total Universities, Average International Outlook.🎨 Technical Implementation & UI/UXGrid-Based Tiled Architecture: Structured horizontal and vertical tiled containers instead of floating elements for consistent alignment, spacing, responsiveness, and clean layout maintenance.Controlled Spacing: Applied padding and negative space between components for a modern interface.Color & Typography: Consistent Teal/Grey visual theme to establish clear visual hierarchy and reduce clutter.Interactive Filtering & Navigation: Filters for university, country, and region, accompanied by navigation elements allowing seamless movement between the four dashboard modules.📈 Key Visualization TechniquesVisualization TypeAnalytical PurposeKPI CardsHigh-level performance summaryBar ChartsRanking and category comparisonLine/Trend ChartsPerformance and productivity trendsScatter PlotsRelationship between analytical variablesPacked Bubble ChartsComparative institutional analysisMapsGeographical distributionBox PlotsDistribution and spread analysisPie ChartsProportional student population comparisonTablesDetailed university-level information🛠️ Technology StackData & Analysis: Microsoft Excel / CSVData Processing: Cleaning, Transformation, Integration, KPI EngineeringData Visualization: Tableau (Worksheets, Dashboards, Filters, Containers, Interactive Navigation)Version Control: Git & GitHub🧠 Key Learnings & CompetenciesData Preparation: Profiling raw datasets, missing-value analysis, cleaning, feature selection, and integration.Data Visualization: Selecting proper visual types, building interactive dashboards, KPI cards, maps, and comparative views.Tableau Expertise: Tiled architecture, container management, navigation, and layout troubleshooting.Analytical Thinking: Translating analytical questions into visualizations, communicating complex datasets through storytelling.💡 Challenges & SolutionsChallenge 1 (Different Sources): QS and THE datasets had varying structures. -> Solution: Integrated and cleaned into a unified analytical structure.Challenge 2 (Missing Data): Raw data contained missing info. -> Solution: Performed thorough missing-value analysis before final selection.Challenge 3 (Column Bloat): Initial dataset had ~55 columns. -> Solution: Filtered down to 44 core analytical columns.Challenge 4 (Layout Stability): Floating elements caused inconsistent spacing. -> Solution: Switched to structured tiled horizontal/vertical containers.Challenge 5 (Complexity): Too many metrics risked clutter. -> Solution: Divided into four focused dashboard modules with summary KPIs.📁 Project StructurePlaintextEduVision_DV/
│
├── dashboard/
│   └── dashboard_preview.png
│
├── data/
│   └── cleaned_university_data_2024.csv
│
├── documentation/
│   └── project_documentation.pdf
│
├── EduVision_DV.twbx
│
└── README.md
📥 How to View the ProjectThe primary deliverable is the Tableau Packaged Workbook (.twbx).Download the Workbook: Get EduVision_DV.twbx from this repository.Open in Tableau: Open the file using Tableau Desktop or Tableau Reader.🎓 Internship ContextProgram: Infosys Springboard 7.0Internship Track: Data VisualizationProject: EduVision_DV — Higher Education Performance Dashboard👤 AuthorShaik SydavaliB.E. — Artificial Intelligence & Machine LearningMethodist College of Engineering and Technology, HyderabadGitHub: github.com/sydavaliEduVision_DV — Turning complex higher-education data into clear, interactive insights. 🎓📊
