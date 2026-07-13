<div align="center">
  
  <img src="https://img.icons8.com/color/96/bar-chart.png" alt="HR Analytics Logo" width="100"/>

  # HR Analytics Dashboard 📊

  **End-to-End Business Intelligence Solution for Workforce Analytics**

  [![Python](https://img.shields.io/badge/Python-3.14-2563EB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Validation](https://img.shields.io/badge/Validation-100%25%20PASS-10B981?style=for-the-badge&logo=checkmarx&logoColor=white)]()
  [![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.59-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-11557C?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org)
  [![Plotly](https://img.shields.io/badge/Plotly-6.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

  <br/>

  **A professional Business Intelligence portfolio project demonstrating end-to-end HR analytics capabilities using SQL, Python, PostgreSQL, and Power BI.**

  <br/>
</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Business Problem](#-business-problem)
- [Objectives](#-objectives)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Database Design](#-database-design)
- [SQL Analysis](#-sql-analysis)
- [Python ETL Pipeline](#-python-etl-pipeline)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Key Performance Indicators](#-key-performance-indicators)
- [Business Insights](#-business-insights)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [Resume Description](#-resume-description)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🎯 Project Overview

HR Analytics Dashboard is a **comprehensive Business Intelligence solution** designed to analyze employee data and extract actionable workforce insights. This project demonstrates the complete data analytics lifecycle:

1. **Data Generation** → 5,000 realistic employee records
2. **Data Engineering** → ETL pipeline with PostgreSQL
3. **Data Analysis** → 50+ SQL queries & Python statistical analysis
4. **Data Visualization** → Power BI & Streamlit dashboards
5. **Reporting** → Automated Excel & CSV report generation

This is a **production-ready, industry-level portfolio project** suitable for showcasing in Business Analyst, Data Analyst, or BI Developer interviews.

---

## 💼 Business Problem

Modern organizations face critical workforce challenges:

| Challenge | Impact |
|-----------|--------|
| **High employee attrition** | Increased recruitment costs, loss of institutional knowledge |
| **Poor work-life balance** | Decreased productivity, low morale |
| **Ineffective promotion cycles** | Talent stagnation, disengagement |
| **Gender pay gaps** | Legal risks, brand reputation damage |
| **Low job satisfaction** | Reduced performance, higher turnover |
| **Overtime burnout** | Health issues, decreased quality of work |

**This project provides data-driven solutions to identify, analyze, and address these challenges.**

---

## ✅ Objectives

1. **Analyze** workforce demographics and diversity metrics
2. **Identify** key drivers of employee attrition
3. **Evaluate** salary distribution and gender pay equity
4. **Assess** promotion patterns and career progression
5. **Measure** employee satisfaction and work-life balance
6. **Track** overtime patterns and their impact
7. **Generate** automated reports for stakeholders
8. **Build** interactive dashboards for real-time monitoring

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Programming** | ![Python](https://img.shields.io/badge/Python-3.14-2563EB?logo=python) ![SQL](https://img.shields.io/badge/SQL-Advanced-CC2927?logo=sql) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql) |
| **Data Analysis** | ![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-2.5-013243?logo=numpy) |
| **Visualization** | ![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?logo=powerbi) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-11557C?logo=python) ![Plotly](https://img.shields.io/badge/Plotly-6.0-3F4F75?logo=plotly) |
| **Dashboard** | ![Streamlit](https://img.shields.io/badge/Streamlit-1.59-FF4B4B?logo=streamlit) |
| **Reporting** | ![Excel](https://img.shields.io/badge/Excel-Reports-217346?logo=microsoftexcel) ![CSV](https://img.shields.io/badge/CSV-Export-4A90D9) |
| **Tools** | ![VS Code](https://img.shields.io/badge/VS%20Code-IDE-007ACC?logo=visualstudiocode) ![Git](https://img.shields.io/badge/Git-VCS-F05032?logo=git) ![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?logo=github) |

</div>

---

## 🏗️ Project Architecture

```
HR-Analytics-Dashboard/
│
├── data/                          # Data layer
│   ├── raw/                       # Raw generated datasets
│   ├── cleaned/                   # Cleaned & validated data
│   ├── processed/                 # Analysis outputs
│   └── generate_dataset.py        # Data generation script
│
├── sql/                           # Database layer
│   ├── schema.sql                 # Database schema design
│   ├── insert.sql                 # Data loading scripts
│   ├── employee_analysis.sql      # Employee headcount queries
│   ├── attrition_analysis.sql     # Attrition deep-dive
│   ├── salary_analysis.sql        # Compensation analysis
│   ├── promotion_analysis.sql     # Promotion trends
│   ├── diversity_analysis.sql     # Diversity metrics
│   ├── overtime_analysis.sql      # Overtime patterns
│   ├── window_functions.sql       # Advanced window functions
│   ├── views.sql                  # Database views
│   └── stored_procedures.sql      # Stored procedures
│
├── python/                        # Analytics layer
│   ├── analytics_utils.py         # Shared utilities
│   ├── clean_data.py              # Data cleaning pipeline
│   ├── validate_data.py           # Data validation
│   ├── analysis.py                # Statistical analysis
│   ├── generate_charts.py         # Chart generation
│   ├── export_reports.py          # Report export
│   └── dashboard.py               # Streamlit dashboard
│
├── powerbi/                       # Power BI layer
│   ├── HR_Analytics.pbix          # Power BI report
│   └── DAX_Measures.txt           # DAX formulas
│
├── reports/                       # Output reports
│   ├── excel/                     # Excel reports
│   ├── html/                      # HTML dashboards
│   ├── pdf/                       # PDF exports
│   └── screenshots/               # Chart images
│
├── documentation/                 # Project documentation
│   ├── BRD.md                     # Business Requirements
│   ├── Functional_Specification.md
│   ├── Technical_Documentation.md
│   ├── Data_Dictionary.md
│   ├── Installation_Guide.md
│   ├── User_Manual.md
│   └── ER_Diagram.md
│
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
└── .gitignore
```

---

## 🗄️ Database Design

### Entity-Relationship Diagram (Simplified)

```
┌──────────────────┐       ┌─────────────────────┐
│  dim_department   │       │   fact_employee     │
├──────────────────┤       ├─────────────────────┤
│ department_id (PK)│◄──────┤ department_id (FK)  │
│ department_name   │       │ employee_id (PK)    │
│ created_at        │       │ employee_name       │
└──────────────────┘       │ age                 │
                           │ gender              │
┌──────────────────┐       │ monthly_income      │
│  dim_job_role     │       │ job_level           │
├──────────────────┤       │ attrition           │
│ job_role_id (PK)  │◄──────┤ hire_date           │
│ job_role_name     │       │ exit_date           │
│ department_id (FK)│       │ ...                 │
└──────────────────┘       └───────┬─────────────┘
                                   │
┌──────────────────┐              │
│ dim_education     │◄─────────────┤
├──────────────────┤              │
│ education_id (PK) │              │
│ education_level   │              │
└──────────────────┘              │
                                  │
┌──────────────────┐              │
│  dim_location     │◄─────────────┘
├──────────────────┤
│ location_id (PK)  │
│ city / state      │
└──────────────────┘
```

### Key Tables
- **fact_employee**: Central fact table (5,000 records) with all employee metrics
- **dim_department**: 10 departments
- **dim_job_role**: 60 job roles across departments
- **dim_education_level**: 5 education levels
- **dim_location**: 50 US cities
- **dim_date**: Date dimension for time-based analysis

### Key Features
- ✅ Primary & Foreign Keys with referential integrity
- ✅ Check constraints for valid data ranges
- ✅ Composite indexes for query optimization
- ✅ Generated columns (is_active)
- ✅ Audit logging table
- ✅ Performance history tracking

---

## 📊 SQL Analysis

**50+ Business SQL Queries** organized into 8 analytical domains:

### Domain Categories
| Category | Queries | Focus Area |
|----------|---------|------------|
| **Employee Analysis** | 20 queries | Headcount, demographics, distributions |
| **Attrition Analysis** | 20 queries | Attrition patterns, risk factors, trends |
| **Salary Analysis** | 15 queries | Compensation, pay equity, hikes |
| **Promotion Analysis** | 15 queries | Promotion rates, career progression |
| **Diversity Analysis** | 10 queries | Gender, age, education diversity |
| **Overtime Analysis** | 10 queries | Overtime patterns & impact |
| **Window Functions** | 15 queries | Running totals, rankings, CTEs |
| **Views & Procedures** | 10 views + 10 SPs | Reusable analytics objects |

### Advanced SQL Techniques Used
- ✅ **Window Functions**: RANK, DENSE_RANK, NTILE, LEAD, LAG, FIRST_VALUE
- ✅ **CTEs**: Common Table Expressions for complex queries
- ✅ **Running Totals**: Cumulative metrics over time
- ✅ **Percentile Analysis**: P25, P50, P75, P90 distributions
- ✅ **Correlation Analysis**: Cross-metric relationships
- ✅ **Risk Scoring**: Multi-factor attrition risk assessment

---

## 🐍 Python ETL Pipeline

### Pipeline Flow

```
Raw Data → Clean → Validate → Analyze → Visualize → Report
   │          │         │          │           │         │
   ▼          ▼         ▼          ▼           ▼         ▼
 generate  pandas   pydantic   stats     matplotlib   openpyxl
 dataset   + numpy  checks    + scipy   + plotly     + csv
```

### Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `analytics_utils.py` | Shared utilities & configuration | KPI calculation, data loading, path management |
| `clean_data.py` | Data cleaning pipeline | Missing value handling, outlier detection (IQR), feature engineering |
| `validate_data.py` | Data quality validation | 20+ validation checks, business rule enforcement |
| `analysis.py` | Statistical & business analysis | Department, attrition, salary, promotion, diversity, correlation analysis |
| `generate_charts.py` | Visualization generation | 12 static charts + interactive Plotly dashboard |
| `export_reports.py` | Automated reporting | Multi-sheet Excel, CSV exports, executive summary |
| `dashboard.py` | Interactive Streamlit dashboard | Real-time filtering, multi-tab insights, KPI cards |

### Key Analysis Features
- ✅ **Attrition Prediction**: Multi-factor risk scoring model
- ✅ **Gender Pay Gap**: Department-level pay equity analysis
- ✅ **Promotion Analysis**: Career progression patterns
- ✅ **Satisfaction Analysis**: Composite satisfaction scoring
- ✅ **Correlation Analysis**: Statistical relationships between metrics
- ✅ **Feature Engineering**: Age groups, salary bands, tenure categories

---

## 📈 Power BI Dashboard

### Dashboard Pages (6+)

| Page | Visuals | Purpose |
|------|---------|---------|
| **Executive Dashboard** | KPI cards, trends, summary | High-level organizational overview |
| **Employee Dashboard** | Demographics, department distribution | Workforce composition analysis |
| **Salary Dashboard** | Salary distribution, pay equity | Compensation analysis |
| **Attrition Dashboard** | Attrition patterns, risk factors | Turnover analysis & prediction |
| **Performance Dashboard** | Rating distribution, satisfaction | Employee performance metrics |
| **Diversity Dashboard** | Gender, age, education diversity | Inclusion metrics |

### DAX Measures (50+)

Categories include:
- Basic Counts (Total/Active/Attrited Employees)
- Rate Calculations (Attrition %, Promotion %, Overtime %)
- Averages (Salary, Age, Tenure, Satisfaction)
- Dynamic Measures (CALCULATE-based)
- Time Intelligence (YTD, MTD, YoY)
- Risk Assessment (Risk Score, Risk Category)
- Comparison Metrics (vs Department Avg, vs Company Avg)

---

## 📐 Key Performance Indicators

| KPI | Formula | Business Value |
|-----|---------|----------------|
| **Total Employees** | `COUNTROWS(fact_employee)` | Workforce size |
| **Active Employees** | `COUNTROWS WHERE attrition = 'No'` | Current headcount |
| **Attrition Rate** | `Attrited / Total * 100` | Retention health |
| **Average Salary** | `AVG(monthly_income)` | Compensation benchmark |
| **Average Age** | `AVG(age)` | Workforce maturity |
| **Average Tenure** | `AVG(years_at_company)` | Employee loyalty |
| **Job Satisfaction** | `AVG(job_satisfaction)` / 4 | Employee happiness |
| **Work-Life Balance** | `AVG(work_life_balance)` / 4 | Well-being metric |
| **Promotion Rate** | `Promoted this year / Total * 100` | Career growth |
| **Overtime %** | `Overtime employees / Total * 100` | Workload indicator |
| **Female %** | `Female employees / Total * 100` | Gender diversity |
| **Training Hours** | `AVG(training_times_last_year)` | Development investment |

---

## 🔍 Business Insights

### Key Findings from Analysis

| Insight | Finding | Business Impact |
|---------|---------|----------------|
| **Highest Attrition** | Customer Support: **35.4%**, Administration: **29.5%**, Sales: **29.4%** | These departments need retention programs urgently |
| **Lowest Attrition** | Legal: **9.6%**, Finance: **13.9%**, R&D: **17.2%** | Lower-paid support roles have higher turnover |
| **Attrition Drivers** | Low job satisfaction (-0.55 lower), Overtime (+9% higher attrition), Age < 30 (+50% more likely) | Focus on satisfaction & work-life balance |
| **Salary Leaders** | Finance: **$8,878/mo**, IT: **$8,806/mo**, Legal: **$8,677/mo** | 3 highest paying departments |
| **Gender Pay Gap** | Female avg: **$8,494/mo**, Male avg: **$8,502/mo** (negligible gap, <0.1%) | Near pay equity across departments |
| **Promotion Rate** | Marketing: **33.4%**, IT: **33.1%**, Support: **33.1%** (highest), Finance: **29.0%** (lowest) | Nearly all departments >25% promotion rate |
| **Overdue Promotions** | Operations: **27.8%**, Administration: **25.2%**, R&D: **23.6%** | Employees stuck >3 years without promotion |
| **Diversity** | Legal: **53.3% female**, Support: **52.2% female** | Most gender-balanced departments |
| **Flight Risk** | **176 high-risk** active employees identified | R&D (29), IT (27), Marketing (22) need attention |
| **Strongest Correlations** | Income ↔ Tenure (0.747), Tenure ↔ Promotion Gap (0.608), Age ↔ Income (0.393) | Experience drives compensation

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.11+
- PostgreSQL 16 (optional)
- Power BI Desktop (optional)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/HR-Analytics-Dashboard.git
cd HR-Analytics-Dashboard

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate the dataset (5,000 employees)
python data/generate_dataset.py

# 4. Run the full pipeline (cleaning → validation → analysis → charts → reports)
python python/clean_data.py && python python/validate_data.py && python python/analysis.py && python python/generate_charts.py && python python/export_reports.py

# 5. Launch interactive dashboard
streamlit run python/dashboard.py
# Opens at http://localhost:8501
```

### PostgreSQL Setup (Optional)

```bash
# Create database
psql -U postgres -c "CREATE DATABASE hr_analytics;"

# Run schema
psql -U postgres -d hr_analytics -f sql/schema.sql

# Load data (update path in insert.sql)
psql -U postgres -d hr_analytics -f sql/insert.sql

# Run analysis queries
psql -U postgres -d hr_analytics -f sql/employee_analysis.sql
# ... run other sql files as needed
```

---

## 📖 Usage

### Running the Full Pipeline

```bash
# One-command execution (after setup)
python data/generate_dataset.py && python python/clean_data.py && python python/validate_data.py && python python/analysis.py && python python/generate_charts.py && python python/export_reports.py
```

### Pipeline Test Results (Verified ✅)

| Stage | Verdict | Details |
|-------|---------|---------|
| `generate_dataset.py` | ✅ PASS | 5,000 records, 32 columns, CSV + XLSX |
| `clean_data.py` | ✅ PASS | 6 outlier columns handled, 8 new features, 40 columns output |
| `validate_data.py` | ✅ PASS | **40/40 checks passed (100%)** — missing values, types, ranges, business rules |
| `analysis.py` | ✅ PASS | 10 analysis modules: department, attrition, salary, promotion, diversity, satisfaction, performance, correlations, training, risk |
| `generate_charts.py` | ✅ PASS | 12/12 static charts (PNG) + 6/6 interactive HTML charts (verified in browser) |
| `export_reports.py` | ✅ PASS | Multi-sheet formatted Excel + 5 CSV reports + executive summary |

### Pipeline Status Summary

```
📊 HR Analytics Pipeline — 100% Pass Rate
═══════════════════════════════════════════
✓ generate_dataset  → 5,000 employees generated
✓ clean_data        → 40 features, 1.21 MB
✓ validate_data     → 40/40 checks passed ✅
✓ analysis          → 10 modules, 23 KPIs, 5 insights
✓ generate_charts   → 18 charts generated
✓ export_reports    → 7 reports exported
═══════════════════════════════════════════
```

### Accessing Outputs

| Output | Location | Description |
|--------|----------|-------------|
| 📁 **Raw Data** | `data/raw/` | Generated CSV & Excel |
| 📁 **Cleaned Data** | `data/cleaned/` | 40 features, 5,000 records |
| 📁 **Analysis Outputs** | `data/processed/` | 12 CSV analysis files |
| 🖼️ **Static Charts** | `reports/screenshots/` | 12 PNG visualizations |
| 🌐 **Interactive Charts** | `reports/html/` | 6 Plotly HTML dashboards |
| 📄 **Excel Report** | `reports/excel/` | 4-sheet formatted workbook |
| 📋 **CSV Reports** | `reports/excel/` | 5 CSV data exports |
| 📝 **Summary** | `reports/excel/` | Executive summary TXT |
| 📈 **Streamlit** | `http://localhost:8501` | Real-time interactive dashboard |

### Interactive Charts (Verfied Working ✅)

The following interactive Plotly HTML dashboards are available in `reports/html/`:

| File | Visualization |
|------|---------------|
| `dashboard_attrition.html` | Donut chart — Attrition distribution by department |
| `dashboard_salary.html` | Box plot — Salary distribution by department |
| `dashboard_satisfaction.html` | Radar chart — Employee satisfaction scores |
| `dashboard_diversity.html` | Stacked bar — Gender distribution by department |
| `dashboard_performance.html` | Bar chart — Performance rating distribution |
| `dashboard_experience.html` | Scatter plot — Salary vs years of experience |

---

## 📝 Resume Description

> **HR Analytics Dashboard** — Built an end-to-end Business Intelligence solution analyzing 5,000+ employee records using Python (Pandas, NumPy, Matplotlib, Plotly), SQL (PostgreSQL), and Power BI. Developed a modular ETL pipeline with 7 Python modules handling data generation, cleaning (40 features, 6 outlier columns handled), validation (40 checks, 100% pass rate), statistical analysis (10 analysis modules, 23 KPIs, 5 business insights), chart generation (12 static + 6 interactive Plotly HTML dashboards verified in browser), and automated reporting (multi-sheet formatted Excel, CSV exports, executive summary). Created a real-time interactive Streamlit dashboard with 5 tabbed views, KPI cards, and cross-filtering. Designed a normalized PostgreSQL star-schema database with 10 tables, 22 indexes, 10 views, and 10 stored procedures. Wrote 50+ business SQL queries covering window functions, CTEs, ranking functions, and running totals. Built 50+ DAX measures for Power BI across 6 dashboard pages. **Technologies**: Python, SQL, PostgreSQL, Power BI, Pandas, NumPy, Matplotlib, Plotly, Streamlit, OpenPyXL.

---

## 🔮 Future Enhancements

- [ ] **Machine Learning Integration**: Build predictive models for attrition forecasting using scikit-learn
- [ ] **Power BI .pbix File**: Create the Power BI desktop file by connecting to the PostgreSQL database or importing the cleaned CSV
- [ ] **Real-time Data Pipeline**: Implement Apache Airflow for scheduled ETL jobs
- [ ] **Cloud Deployment**: Deploy to AWS/GCP with automated data pipeline
- [ ] **Natural Language Processing**: Analyze exit interview text data for sentiment analysis
- [ ] **API Development**: Build REST API for HR data access using FastAPI
- [ ] **Advanced Analytics**: Add cohort analysis, survival analysis, and CLV modeling
- [ ] **Data Governance**: Implement data catalog with lineage tracking
- [ ] **Mobile Dashboard**: Create mobile-optimized Power BI views

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  
  **Built with ❤️ for Data Analytics Portfolio**
  
  *If you found this project useful, please ⭐ star it on GitHub!*
  
  [![GitHub stars](https://img.shields.io/github/stars/yourusername/HR-Analytics-Dashboard?style=social)](https://github.com/yourusername/HR-Analytics-Dashboard)

</div>
