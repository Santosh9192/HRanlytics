# Functional Specification Document

## HR Analytics Dashboard

---

## 1. Introduction

### 1.1 Purpose
This Functional Specification Document (FSD) describes the detailed functional requirements, system behavior, user interactions, and output specifications for the HR Analytics Dashboard project.

### 1.2 Scope
This document covers all functional aspects of the HR analytics solution including data generation, database design, ETL pipeline, analytics modules, visualization, and reporting.

---

## 2. System Features

### Feature 1: Data Generation
**ID**: F-DG-001

**Description**: Generate realistic synthetic HR dataset with 5,000 employee records.

**Input Parameters**:
- Number of employees: 5,000 (configurable)
- Random seed: 42 (reproducible)

**Output**:
- `data/raw/hr_data.csv`: CSV format
- `data/raw/hr_data.xlsx`: Excel format

**Data Columns** (32 fields):
- Identification: EmployeeID, EmployeeName
- Demographics: Age, Gender, MaritalStatus
- Organizational: Department, JobRole, JobLevel
- Compensation: MonthlyIncome, PercentSalaryHike, StockOptionLevel
- Experience: YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion
- Satisfaction: JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance, RelationshipSatisfaction
- Performance: PerformanceRating, TrainingTimesLastYear
- Employment: Attrition, HireDate, ExitDate, OverTime, BusinessTravel
- Location: City, State, Country, DistanceFromHome

**Business Rules**:
- Age: 22-61 years
- Income: $3,000-$25,000/month (varies by job level)
- Attrition rate: ~15-30% (varies by department)
- 10 departments with 60 job roles
- Employee names from realistic US name database

---

### Feature 2: Data Cleaning
**ID**: F-DC-001

**Description**: Clean raw HR data through automated ETL pipeline.

**Pipeline Stages**:
1. **Load**: Import CSV data
2. **Missing Values**: 
   - Numeric: median imputation
   - Categorical: mode imputation
   - Critical columns: drop if missing
3. **Duplicates**: 
   - Exact duplicate removal
   - EmployeeID-based deduplication
4. **Data Types**:
   - Integer columns: Int64
   - Float columns: float64
   - Date columns: datetime64
   - Categorical columns: category type
5. **Outliers**:
   - IQR method (1.5x)
   - Winsorization (cap at bounds)
6. **Feature Engineering**:
   - AgeGroup, SalaryRange, TenureGroup
   - ExperienceScore, SatisfactionScore
   - PerformanceScore, AttritionFlag
   - IsRemoteWorker

**Output**: `data/cleaned/hr_data_cleaned.csv`

---

### Feature 3: Data Validation
**ID**: F-DV-001

**Description**: Validate data quality and integrity.

**Validation Categories**:

| Category | Checks | Pass Criteria |
|----------|--------|---------------|
| Missing Values | 20 columns | < 5% missing per column |
| Numeric Types | 15 columns | 100% valid numeric |
| Date Validity | 2 columns | 100% valid dates |
| Range Checks | 10 fields | Within defined ranges |
| Uniqueness | EmployeeID | 100% unique |
| Business Rules | 5 rules | 100% compliance |

**Output**: Validation report with pass/fail status for each check
**Target**: >95% overall pass rate

---

### Feature 4: Database Management
**ID**: F-DB-001

**Description**: PostgreSQL database with normalized schema.

**Schema Components**:
- `dim_department`: 10 departments
- `dim_job_role`: 60 job roles
- `dim_education_level`: 5 levels
- `dim_location`: City/State dimensions
- `dim_date`: Date dimension (2000-2026)
- `fact_employee`: 5,000 employee records
- `fact_performance_history`: Performance tracking

**Database Features**:
- Primary keys with auto-increment
- Foreign keys with referential integrity
- Check constraints for data validation
- 22 performance indexes
- Generated columns (is_active)
- Audit logging table

---

### Feature 5: SQL Analytics
**ID**: F-SA-001

**Description**: 50+ business SQL queries for comprehensive analysis.

**Query Categories**:

| Category | Count | Example Queries |
|----------|-------|-----------------|
| Employee Analysis | 20 | Headcount, demographics, distributions |
| Attrition Analysis | 20 | Attrition rates, risk factors, trends |
| Salary Analysis | 15 | Compensation stats, pay equity |
| Promotion Analysis | 15 | Promotion rates, delays, correlations |
| Diversity Analysis | 10 | Gender, age, education diversity |
| Overtime Analysis | 10 | Overtime patterns, impact analysis |
| Window Functions | 15 | Rankings, running totals, CTEs |
| Views | 10 | Reusable analytical views |
| Stored Procedures | 10 | Automated maintenance & reporting |

---

### Feature 6: Python Analysis
**ID**: F-PA-001

**Description**: Statistical and business analysis modules.

**Analysis Modules**:

1. **Department Analysis**
   - Employee count, average salary, attrition rate
   - Overtime percentage, gender diversity
   
2. **Attrition Deep-Dive**
   - Attrition rate by all dimensions
   - Attrited vs Active comparison
   - Risk factor identification
   
3. **Salary Analysis**
   - Salary distribution statistics
   - Gender pay gap calculation
   - Education and experience premiums
   
4. **Promotion Analysis**
   - Promotion rate by department
   - Overdue promotion identification
   - Career progression patterns
   
5. **Diversity Metrics**
   - Gender diversity score
   - Age distribution analysis
   - Education field diversity
   
6. **Correlation Analysis**
   - Cross-metric correlation matrix
   - Strongest relationship identification
   
7. **Risk Assessment**
   - Multi-factor risk scoring
   - High/Medium/Low risk classification

---

### Feature 7: Visualization
**ID**: F-VZ-001

**Description**: Generate charts and interactive dashboards.

**Static Charts** (Matplotlib, 12 charts):
1. Employee Distribution by Department (bar)
2. Gender Diversity by Department (stacked bar)
3. Attrition Rate by Department (horizontal bar)
4. Salary Distribution by Department (bar with error bars)
5. Age Distribution (histogram)
6. Satisfaction Scores (bar chart)
7. Performance vs Salary (box plot)
8. Overtime Impact on Attrition (bar chart)
9. Promotion Analysis (bar chart)
10. Correlation Heatmap
11. Monthly Hiring Trend (line chart)
12. Education vs Salary (bar chart)

**Interactive Dashboard** (Plotly HTML):
- Attrition pie chart
- Salary box plot by department
- Satisfaction radar chart
- Gender diversity stacked bar
- Performance distribution
- Salary vs experience scatter plot

**Streamlit Dashboard**:
- 5-tab interface (Overview, Attrition, Salary, Performance, Diversity)
- Real-time filtering by department, gender, attrition status
- KPI metric cards
- Interactive charts and data table

---

### Feature 8: Reporting
**ID**: F-RP-001

**Description**: Automated report generation.

**Excel Reports**:
- KPI Summary sheet
- Department Analysis sheet
- Attrition Analysis sheet
- Salary Analysis sheet
- Formatted headers, borders, alternating row colors

**CSV Reports**:
- Employee data export
- Department summary
- Attrition data
- Active employees
- Salary summary

**Summary Report**:
- Executive summary text file
- KPI section
- Department highlights
- Top business insights

---

## 3. User Interface Specifications

### 3.1 Streamlit Dashboard

**Layout**:
- Sidebar: Filters and navigation
- Main: 5 tabbed sections
- KPI cards in metrics

**User Interactions**:
1. Select department filter (dropdown)
2. Select gender filter (dropdown)
3. Select attrition status (radio buttons)
4. Navigate between tabs
5. View interactive charts
6. Scroll through employee data table

### 3.2 Power BI Dashboard (6 pages)

1. **Executive Dashboard**: KPI cards, high-level metrics
2. **Employee Dashboard**: Demographics, department distribution
3. **Salary Dashboard**: Compensation analysis, pay equity
4. **Attrition Dashboard**: Attrition patterns, risk analysis
5. **Performance Dashboard**: Performance and satisfaction
6. **Diversity Dashboard**: Inclusion metrics

---

## 4. Output Specifications

### 4.1 Data Files
| File | Format | Location |
|------|--------|----------|
| Raw HR Data | CSV, XLSX | data/raw/ |
| Cleaned HR Data | CSV | data/cleaned/ |
| Analysis Results | CSV | data/processed/ |

### 4.2 Reports
| Report | Format | Location |
|--------|--------|----------|
| Executive Summary | TXT | reports/excel/ |
| Full Analytics Report | XLSX | reports/excel/ |
| Department Summary | CSV | reports/excel/ |
| Attrition Report | CSV | reports/excel/ |
| Salary Analysis | CSV | reports/excel/ |

### 4.3 Visualizations
| Type | Format | Location |
|------|--------|----------|
| Static Charts | PNG | reports/screenshots/ |
| Interactive Dashboard | HTML | reports/html/ |

### 4.4 Documentation
| Document | Format | Location |
|----------|--------|----------|
| All Documentation | MD | documentation/ |

---

## 5. Error Handling

| Scenario | Error Response |
|----------|---------------|
| Missing data file | FileNotFoundError with path info |
| Invalid data format | Descriptive error message |
| Database connection failure | Connection timeout with retry |
| Validation failure | Detailed failure report |
| Chart generation error | Error caught, process continues |

---

## 6. Performance Requirements

| Operation | Performance Target |
|-----------|-------------------|
| Dataset generation | < 30 seconds |
| Data cleaning | < 10 seconds |
| Data validation | < 5 seconds |
| Full analysis | < 30 seconds |
| Chart generation | < 20 seconds |
| Report export | < 15 seconds |
| Dashboard load | < 3 seconds |
| Database queries | < 5 seconds |

---

## 7. Security Considerations

- No PII (Personally Identifiable Information) - synthetic data only
- No external API connections required
- Local execution environment
- No authentication/authorization required for local deployment
- Database credentials stored in environment variables (optional)

---

## 8. Dependencies

### Software Dependencies
- Python 3.11+
- PostgreSQL 16+ (optional)
- Power BI Desktop (optional)
- Git

### Python Package Dependencies
- pandas, numpy (data processing)
- matplotlib, plotly (visualization)
- openpyxl (Excel export)
- faker (data generation)
- streamlit (interactive dashboard)
- scipy (advanced statistics)
- psycopg2-binary, sqlalchemy (database, optional)

---

## 9. Glossary

| Term | Definition |
|------|------------|
| Attrition | Employee turnover/voluntary departure |
| ETL | Extract, Transform, Load |
| KPI | Key Performance Indicator |
| IQR | Interquartile Range |
| DAX | Data Analysis Expressions (Power BI) |
| Dimension | Descriptive attribute table |
| Fact Table | Central quantitative data table |
| Winsorization | Capping outliers at percentile bounds |
