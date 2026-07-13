# User Manual

## HR Analytics Dashboard

---

## 1. Introduction

Welcome to the HR Analytics Dashboard! This user manual provides step-by-step instructions for using the HR analytics system, including data generation, analysis execution, report viewing, and dashboard navigation.

---

## 2. Getting Started

### 2.1 System Overview

The HR Analytics system consists of:

1. **Dataset Generator**: Creates realistic employee data
2. **ETL Pipeline**: Cleans and validates data
3. **Analysis Engine**: Performs statistical analysis
4. **Report Generator**: Creates Excel and CSV reports
5. **Chart Generator**: Produces visualizations
6. **Interactive Dashboard**: Real-time data exploration

### 2.2 Quick Navigation

| If you want to... | Then... |
|-------------------|---------|
| Generate employee data | `python data/generate_dataset.py` |
| Clean the dataset | `python python/clean_data.py` |
| View validation results | `python python/validate_data.py` |
| Run all analysis | `python python/analysis.py` |
| Create charts | `python python/generate_charts.py` |
| Export reports | `python python/export_reports.py` |
| Open interactive dashboard | `streamlit run python/dashboard.py` |

---

## 3. Running the Pipeline

### 3.1 Step 1: Generate Dataset

```bash
python data/generate_dataset.py
```

**What happens**: Creates 5,000 employee records with realistic demographics, compensation, satisfaction scores, and attrition patterns.

**Output**:
- `data/raw/hr_data.csv` - CSV format
- `data/raw/hr_data.xlsx` - Excel format

**Console Output**:
```
============================================================
  HR Analytics Dataset Generator
============================================================

Generating 5000 employee records...
[OK] Generated 5000 records successfully.
...
```

### 3.2 Step 2: Clean Data

```bash
python python/clean_data.py
```

**What happens**: 
- Handles missing values
- Removes duplicates
- Corrects data types
- Handles outliers using IQR method
- Creates new features (age groups, salary ranges, etc.)

**Output**: `data/cleaned/hr_data_cleaned.csv`

### 3.3 Step 3: Validate Data

```bash
python python/validate_data.py
```

**What happens**: Runs 20+ quality checks against the dataset.

**Output**:
- Console: Pass/Fail report
- File: `data/cleaned/validation_report.json`

### 3.4 Step 4: Run Analysis

```bash
python python/analysis.py
```

**What happens**: Runs comprehensive analysis including:
- Department analysis
- Attrition deep-dive
- Salary analysis
- Promotion trends
- Diversity metrics
- Satisfaction analysis
- Performance analysis
- Correlation analysis
- Risk assessment

**Output**: Multiple CSV files in `data/processed/`

### 3.5 Step 5: Generate Charts

```bash
python python/generate_charts.py
```

**What happens**: Creates 12 static charts and 1 interactive dashboard.

**Output**:
- PNG charts in `reports/screenshots/`
- HTML dashboard in `reports/html/`

### 3.6 Step 6: Export Reports

```bash
python python/export_reports.py
```

**What happens**: Creates formatted Excel and CSV reports.

**Output**:
- Excel: `reports/excel/HR_Analytics_Report.xlsx`
- CSV: Multiple files in `reports/excel/`
- Summary: `reports/excel/executive_summary.txt`

---

## 4. Using the Interactive Dashboard

### 4.1 Launching

```bash
streamlit run python/dashboard.py
```

The dashboard opens in your default web browser at `http://localhost:8501`.

### 4.2 Dashboard Overview

**Layout**:
- **Left Sidebar**: Filters and navigation
- **Main Area**: Tabbed content with KPIs and charts
- **Top**: KPI metric cards

### 4.3 Using Filters

1. **Department Filter**: Select a specific department or view all
2. **Gender Filter**: Filter by male/female
3. **Attrition Filter**: View all, active only, or attrited only

Filters apply to all charts and metrics on every tab.

### 4.4 Tab Navigation

#### Tab 1: Overview
- Department distribution bar chart
- Gender distribution pie chart
- Age distribution histogram
- Key KPI metrics

#### Tab 2: Attrition
- Attrition rate by department
- Attrition by multiple factors
- Attrition trends

#### Tab 3: Salary
- Salary by department
- Salary vs performance scatter plot
- Compensation analysis

#### Tab 4: Performance
- Performance distribution
- Satisfaction scores
- Training analysis

#### Tab 5: Diversity
- Gender diversity by department
- Education field distribution
- Diversity metrics

### 4.5 Interpreting KPI Cards

The top of the dashboard displays 5 KPI cards:

| KPI | What It Shows |
|-----|---------------|
| Total Employees | Total count + active count |
| Attrition Rate | Percentage + number who left |
| Avg Salary | Mean salary + median |
| Avg Age | Average age + average tenure |
| Avg Satisfaction | Job satisfaction + work-life balance |

---

## 5. Understanding Analysis Outputs

### 5.1 Department Analysis

Located in: `data/processed/department_analysis.csv`

**Columns**:
- `department`: Department name
- `employee_count`: Number of employees
- `avg_salary`: Average monthly income
- `avg_age`: Average employee age
- `attrition_rate`: Percentage who left
- `overtime_pct`: Percentage working overtime

### 5.2 Attrition Analysis

Located in: `data/processed/attrition_by_department.csv`, `data/processed/attrition_comparison.csv`

**Key Metrics**:
- Attrition rate by department
- Attrited vs Active employee comparison
- Attrition by gender, overtime, marital status

### 5.3 Salary Analysis

Located in: `data/processed/salary_by_department.csv`

**Key Metrics**:
- Average, median, min, max salary
- Standard deviation
- Gender pay gap

### 5.4 Business Insights

Located in: `data/processed/business_insights.csv`

**What it contains**: Actionable findings such as:
- Departments with highest attrition
- Factors most correlated with attrition
- Salary disparities
- Promotion bottlenecks

---

## 6. Viewing Reports

### 6.1 Excel Report

Open `reports/excel/HR_Analytics_Report.xlsx` in Microsoft Excel or any spreadsheet application.

**Sheets**:
1. **KPI Summary**: Key metrics at a glance
2. **Department Analysis**: Department-level KPIs
3. **Attrition Analysis**: Attrition breakdowns
4. **Salary Analysis**: Compensation details

### 6.2 Summary Report

Open `reports/excel/executive_summary.txt` in any text editor.

Contains a formatted summary with:
- All KPIs
- Department highlights
- Top 5 business insights

### 6.3 Charts

View saved charts in `reports/screenshots/` as PNG images:

| File | Description |
|------|-------------|
| `employee_distribution.png` | Employees by department |
| `gender_diversity.png` | Gender diversity stacked bar |
| `attrition_rate.png` | Attrition by department |
| `salary_distribution.png` | Salary by department |
| `age_distribution.png` | Age histogram |
| `satisfaction_scores.png` | Satisfaction scores |
| `performance_vs_salary.png` | Box plot |
| `overtime_impact.png` | Attrition by overtime |
| `promotion_analysis.png` | Years since promotion |
| `correlation_heatmap.png` | Correlation matrix |
| `monthly_hiring_trend.png` | Hiring trend line |
| `education_salary.png` | Education vs salary |

---

## 7. Power BI Dashboard (Optional)

### 7.1 Opening the Dashboard

1. Launch Power BI Desktop
2. Open `powerbi/HR_Analytics.pbix`

### 7.2 Dashboard Pages

| Page | Visuals | How to Use |
|------|---------|------------|
| **Executive Dashboard** | KPI cards, line charts | View high-level metrics |
| **Employee Dashboard** | Bar charts, treemap | Explore demographics |
| **Salary Dashboard** | Box plot, scatter | Analyze compensation |
| **Attrition Dashboard** | Pie chart, matrix | Understand turnover |
| **Performance Dashboard** | Gauges, bar charts | Review performance |
| **Diversity Dashboard** | Stacked bar, map | Monitor diversity |

### 7.3 Using Slicers

Use slicers to filter data:
- Click on slicer values to filter all visuals on the page
- CTRL+click to select multiple values
- Clear filter using the eraser icon

---

## 8. Frequently Asked Questions

### Q: How long does it take to generate the dataset?
A: Approximately 10-30 seconds for 5,000 records.

### Q: Can I generate more than 5,000 records?
A: Yes, modify `NUM_EMPLOYEES` in `data/generate_dataset.py`.

### Q: Where are the cleaned data files?
A: In `data/cleaned/hr_data_cleaned.csv`.

### Q: How do I view the interactive dashboard?
A: Run `streamlit run python/dashboard.py` and open `http://localhost:8501`.

### Q: Do I need PostgreSQL?
A: No, PostgreSQL is optional. The Python pipeline works standalone.

### Q: How do I create a Power BI dashboard?
A: Connect Power BI to the PostgreSQL database or import the CSV files.

### Q: Can I customize the charts?
A: Yes, modify colors, labels, and styles in `python/generate_charts.py`.

---

## 9. Tips & Best Practices

1. **Run the full pipeline** in sequence for best results
2. **Use the virtual environment** to avoid package conflicts
3. **Check validation reports** to ensure data quality
4. **Review business insights** for actionable findings
5. **Customize NUM_EMPLOYEES** for different dataset sizes
6. **Update colors in PALETTE** in `generate_charts.py` for branding
7. **Add new SQL queries** in the `sql/` directory for extended analysis
8. **Combine filters** in the Streamlit dashboard for deep-dive analysis

---

## 10. Support

For issues or questions:

1. Check the Troubleshooting section in the Installation Guide
2. Review error messages in the console output
3. Verify all Python packages are installed
4. Ensure you're running from the project root directory
5. Check that input files exist before running dependent scripts
