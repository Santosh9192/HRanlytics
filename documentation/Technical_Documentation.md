# Technical Documentation

## HR Analytics Dashboard

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                           │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  data/raw/      │  │ data/cleaned/ │  │ data/processed/│  │
│  │  hr_data.csv    │  │ hr_cleaned.csv│  │ analysis_*.csv │  │
│  └────────┬────────┘  └──────┬───────┘  └───────┬───────┘  │
│           │                  │                   │          │
└───────────┼──────────────────┼───────────────────┼──────────┘
            │                  │                   │
┌───────────┼──────────────────┼───────────────────┼──────────┐
│           ▼                  ▼                   ▼          │
│                    APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Python ETL & Analysis Pipeline                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │clean_data│→ │validate  │→ │analysis  │          │  │
│  │  │  .py     │  │  _data.py│  │   .py    │          │  │
│  │  └──────────┘  └──────────┘  └────┬─────┘          │  │
│  │         ┌─────────────────────────┼──────────┐     │  │
│  │         ▼                         ▼          ▼     │  │
│  │  ┌────────────┐  ┌─────────────┐  ┌────────────┐  │  │
│  │  │generate    │  │export_      │  │dashboard   │  │  │
│  │  │_charts.py  │  │reports.py   │  │   .py      │  │  │
│  │  └────────────┘  └─────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼──────────────────────────────┐
│                             ▼                              │
│                    PRESENTATION LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Power BI    │  │  Streamlit   │  │  Static Reports  │ │
│  │  Dashboard   │  │  Dashboard   │  │  Excel, CSV, PDF │ │
│  │  (.pbix)     │  │  (.py)       │  │  (.xlsx, .csv)   │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack Details

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Core programming language |
| **Database** | PostgreSQL | 16 | Data warehousing |
| **Data Processing** | Pandas | 2.0+ | Data manipulation |
| **Numerical Analysis** | NumPy | 1.24+ | Statistical computations |
| **Static Charts** | Matplotlib | 3.7+ | PNG chart generation |
| **Interactive Charts** | Plotly | 5.15+ | HTML interactive charts |
| **Excel Export** | OpenPyXL | 3.1+ | Formatted Excel reports |
| **Interactive Dashboard** | Streamlit | 1.28+ | Real-time dashboard |
| **Data Generation** | Faker | 20.0+ | Synthetic data creation |
| **Data Validation** | Custom | — | Business rule validation |
| **BI Tool** | Power BI | Desktop | Professional dashboards |
| **Version Control** | Git | Latest | Source code management |

---

## 2. Database Schema Design

### 2.1 Entity Relationship

The database follows a **star schema** design with one fact table and multiple dimension tables:

**Fact Table**: `fact_employee` (5,000 rows)
**Dimension Tables**: `dim_department`, `dim_job_role`, `dim_education_level`, `dim_location`, `dim_date`

### 2.2 Table Specifications

#### fact_employee
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| employee_id | INTEGER | PRIMARY KEY | Unique employee identifier |
| employee_name | VARCHAR(200) | NOT NULL | Full name |
| age | INTEGER | CHECK (18-80) | Employee age |
| gender | VARCHAR(10) | CHECK (Male/Female) | Gender |
| department_id | INTEGER | FK→dim_department | Department reference |
| job_role_id | INTEGER | FK→dim_job_role | Job role reference |
| education_level_id | INTEGER | FK→dim_education | Education level |
| education_field | VARCHAR(100) | — | Field of study |
| marital_status | VARCHAR(20) | CHECK | Marital status |
| monthly_income | NUMERIC(10,2) | CHECK > 0 | Monthly salary |
| job_level | INTEGER | CHECK (1-5) | Job seniority level |
| years_at_company | INTEGER | DEFAULT 0 | Total tenure |
| years_in_current_role | INTEGER | DEFAULT 0 | Time in current role |
| years_since_last_promotion | INTEGER | DEFAULT 0 | Time since last promotion |
| years_with_current_manager | INTEGER | DEFAULT 0 | Time with current manager |
| distance_from_home | INTEGER | DEFAULT 0 | Commute distance |
| business_travel | VARCHAR(50) | CHECK | Travel frequency |
| overtime | VARCHAR(5) | CHECK (Yes/No) | Overtime status |
| environment_satisfaction | INTEGER | CHECK (1-4) | Environment satisfaction |
| job_satisfaction | INTEGER | CHECK (1-4) | Job satisfaction |
| relationship_satisfaction | INTEGER | CHECK (1-4) | Relationship satisfaction |
| work_life_balance | INTEGER | CHECK (1-4) | Work-life balance |
| performance_rating | INTEGER | CHECK (1-4) | Performance rating |
| training_times_last_year | INTEGER | DEFAULT 0 | Training sessions |
| stock_option_level | INTEGER | CHECK (0-3) | Stock option level |
| percent_salary_hike | NUMERIC(5,1) | DEFAULT 0 | Last salary hike % |
| attrition | VARCHAR(5) | CHECK (Yes/No) | Attrition status |
| hire_date | DATE | NOT NULL | Hire date |
| exit_date | DATE | — | Exit date (if applicable) |
| location_id | INTEGER | FK→dim_location | Location reference |
| is_active | BOOLEAN | GENERATED | Computed active status |

### 2.3 Indexes

- **Primary**: `employee_id`, `department_id`, `job_role_id`
- **Performance**: 22 indexes on frequently queried columns
- **Composite**: Department+Attrition, Department+Gender, Department+Income

---

## 3. SQL Implementation Details

### 3.1 Query Categories

#### Employee Analysis (20 queries)
- Basic counts and distributions
- Department-level demographics
- Age group and generation analysis
- Location and travel patterns

#### Attrition Analysis (20 queries)
- Multi-dimensional attrition breakdowns
- Risk factor analysis (satisfaction, overtime, income)
- Attrition vs retention comparison
- Flight risk scoring model

#### Salary Analysis (15 queries)
- Statistical salary distributions
- Gender pay gap analysis
- Education and experience premiums
- Compensation ratio analysis

#### Window Functions (15 queries)
- `RANK()` / `DENSE_RANK()` for department rankings
- `NTILE()` for quartile/percentile analysis
- `LEAD()` / `LAG()` for year-over-year comparisons
- `FIRST_VALUE()` / `LAST_VALUE()` for boundary analysis
- Running totals and moving averages

### 3.2 Views (10)

| View Name | Purpose |
|-----------|---------|
| `v_employee_details` | Complete employee information |
| `v_department_summary` | Aggregated department KPIs |
| `v_attrition_analysis` | Attrition details with tenure |
| `v_salary_distribution` | Salary percentiles by department/role |
| `v_performance_overview` | Performance with labels |
| `v_diversity_dashboard` | Gender/age/education diversity |
| `v_employee_tenure` | Tenure categories and promotion status |
| `v_monthly_headcount` | Monthly headcount trends |
| `v_training_analysis` | Training and performance correlation |
| `v_employee_risk_assessment` | Multi-factor risk scoring |

### 3.3 Stored Procedures (10)

| Procedure | Purpose |
|-----------|---------|
| `sp_refresh_employee_status` | Update is_active flags |
| `sp_calculate_dept_attrition` | Department attrition calculation |
| `sp_department_salary_report` | Salary report by department |
| `sp_attrition_risk_assessment` | Flight risk scoring |
| `sp_monthly_kpi_snapshot` | Monthly KPI snapshot |
| `sp_promotion_eligible` | Promotion eligibility check |
| `sp_update_employee_salary` | Salary update with audit |
| `sp_headcount_report` | Headcount report by date |
| `sp_data_quality_check` | Data quality validation |
| `sp_yearly_attrition_report` | Annual attrition report |

---

## 4. Python Modules

### 4.1 Module Dependencies

```
analytics_utils.py
    ├── clean_data.py
    ├── validate_data.py
    ├── analysis.py
    ├── generate_charts.py
    ├── export_reports.py
    └── dashboard.py
```

### 4.2 Module Specifications

#### analytics_utils.py
- **Purpose**: Shared utilities and configuration
- **Key Classes/Functions**: `load_raw_data()`, `calculate_kpis()`, `standardize_columns()`
- **Constants**: Path configurations, column mappings, label dictionaries
- **Helper Functions**: `get_age_group()`, `get_salary_range()`, `get_risk_category()`

#### clean_data.py
- **Purpose**: Data cleaning ETL pipeline
- **Pipeline Steps**:
  1. Load raw data
  2. Handle missing values (median/mode imputation)
  3. Remove duplicates (exact and ID-based)
  4. Correct data types (int, float, datetime, categorical)
  5. Handle outliers (IQR method with winsorization)
  6. Feature engineering (age groups, salary bands, tenure categories)

#### validate_data.py
- **Purpose**: Data quality validation
- **Validation Categories**:
  - Missing data (20 checks)
  - Data types (numeric, date validity)
  - Range checks (age 18-80, salary > 0, satisfaction 1-4)
  - Uniqueness (Employee ID)
  - Business rules (attrition-exit date consistency)
  - Statistical outliers

#### analysis.py
- **Purpose**: Comprehensive business analysis
- **Class**: `HRDataAnalyzer` with methods:
  - `analyze_departments()` - Department KPIs
  - `analyze_attrition()` - Attrition deep-dive
  - `analyze_salary()` - Compensation analysis
  - `analyze_promotion()` - Promotion trends
  - `analyze_diversity()` - Diversity metrics
  - `analyze_satisfaction()` - Satisfaction scores
  - `analyze_performance()` - Performance ratings
  - `analyze_correlations()` - Statistical correlations
  - `risk_assessment()` - Flight risk scoring

#### generate_charts.py
- **Purpose**: Chart generation
- **12 Static Charts** (Matplotlib PNG)
- **1 Interactive Dashboard** (Plotly HTML)
- Chart types: bar, pie, histogram, box plot, heatmap, scatter, radar

#### export_reports.py
- **Purpose**: Report generation
- **Excel Reports**: Multi-sheet formatted workbooks
- **CSV Reports**: Raw data exports by category
- **Summary Report**: Text-based executive summary

#### dashboard.py
- **Purpose**: Interactive Streamlit dashboard
- **Tabs**: Overview, Attrition, Salary, Performance, Diversity
- **Features**: Filters, KPI cards, real-time charts, data table

---

## 5. Data Flow

### 5.1 ETL Pipeline Flow

```
START
  │
  ▼
┌─────────────────────┐
│  generate_dataset   │   Creates 5,000 employee records
│  (data/generate_    │   Output: data/raw/hr_data.csv
│   dataset.py)       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  clean_data.py      │   Handles missing values, duplicates,
│                     │   outliers, data types, features
│                     │   Output: data/cleaned/hr_data_cleaned.csv
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  validate_data.py   │   20+ validation checks
│                     │   Output: Validation report JSON
└─────────┬───────────┘
          │
          ├──────────────────────────┐
          │                          │
          ▼                          ▼
┌─────────────────────┐   ┌─────────────────────┐
│  analysis.py        │   │  generate_charts.py  │
│                     │   │                      │
│ Department Analysis │   │ 12 Static Charts     │
│ Attrition Analysis  │   │ Interactive Dashboard│
│ Salary Analysis     │   │                      │
│ Promotion Analysis  │   │ Output: PNG, HTML    │
│ Diversity Analysis  │   └─────────┬────────────┘
│ Correlation Analysis│             │
│                     │             │
│ Output: CSV files   │             │
└─────────┬───────────┘             │
          │                         │
          ▼                         │
┌─────────────────────┐             │
│  export_reports.py  │◄────────────┘
│                     │
│ Excel Workbooks     │
│ CSV Reports         │
│ Summary Report      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  dashboard.py       │   Streamlit interactive dashboard
│  (Optional)         │   Real-time visualization
└─────────────────────┘
```

---

## 6. Configuration

### 6.1 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `hr_analytics` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | — |
| `DATA_DIR` | Data directory path | `./data` |
| `OUTPUT_DIR` | Reports output path | `./reports` |

### 6.2 File Paths

All paths are configured in `analytics_utils.py` and are relative to the project root directory.

---

## 7. Testing Strategy

| Test Type | Coverage | Method |
|-----------|----------|--------|
| Data Validation | 20+ business rules | validate_data.py |
| Schema Validation | All constraints | SQL schema checks |
| KPI Accuracy | Cross-validation | Python vs SQL comparison |
| Data Quality | Pass rate > 95% | Automated checks |
| Pipeline Integrity | End-to-end | Sequential execution |

---

## 8. Performance Considerations

- **Database Indexing**: 22 indexes on frequently queried columns
- **Composite Indexes**: Multi-column indexes for common join patterns
- **Query Optimization**: Window functions vs self-joins
- **Memory Management**: Chunked processing for large datasets
- **Caching**: Streamlit caching for dashboard performance

---

## 9. Deployment

### 9.1 Local Deployment
```bash
git clone <repo-url>
cd HR-Analytics-Dashboard
pip install -r requirements.txt
python data/generate_dataset.py
python -m python.clean_data
python -m python.analysis
streamlit run python/dashboard.py
```

### 9.2 PostgreSQL Integration
```bash
createdb hr_analytics
psql -d hr_analytics -f sql/schema.sql
psql -d hr_analytics -f sql/insert.sql
```
