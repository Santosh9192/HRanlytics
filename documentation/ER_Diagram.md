# Entity-Relationship Diagram

## HR Analytics Database

---

## 1. Overview

This document describes the Entity-Relationship (ER) design for the HR Analytics PostgreSQL database. The database follows a **star schema** dimensional modeling approach optimized for analytical queries.

---

## 2. ER Diagram (Textual)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   ┌──────────────────────┐              ┌──────────────────────────┐    │
│   │   dim_department      │              │     dim_education_level   │    │
│   ├──────────────────────┤              ├──────────────────────────┤    │
│   │ PK department_id     │◄────────┐   │ PK education_level_id    │◄┐   │
│   │    department_name    │         │   │    education_level       │ │   │
│   │    created_at         │         │   │    description           │ │   │
│   └──────────────────────┘         │   └──────────────────────────┘ │   │
│                                     │                               │   │
│   ┌──────────────────────┐         │   ┌──────────────────────────┐ │   │
│   │   dim_job_role        │         │   │      dim_location         │ │   │
│   ├──────────────────────┤         │   ├──────────────────────────┤ │   │
│   │ PK job_role_id       │◄────┐   │   │ PK location_id           │◄┤   │
│   │    job_role_name      │    │   │   │    city                   │ │   │
│   │ FK department_id      │────┘   │   │    state                  │ │   │
│   │    created_at          │        │   │    country                │ │   │
│   └──────────────────────┘        │   └──────────────────────────┘ │   │
│                                     │                               │   │
│   ┌────────────────────────────────────────────────────────────────┐ │   │
│   │                      fact_employee                              │ │   │
│   ├────────────────────────────────────────────────────────────────┤ │   │
│   │ PK employee_id                                                 │ │   │
│   │    employee_name, age, gender                                  │ │   │
│   │ FK department_id            ───────────────────────────────────┘ │   │
│   │ FK job_role_id             ─────────────────────────────────────┘   │
│   │ FK education_level_id      ───────────────────────────────────────┘
│   │ FK location_id             ─────────────────────────────────────┘
│   │    education_field, marital_status                                │
│   │    monthly_income, job_level                                      │
│   │    years_at_company, years_in_current_role                        │
│   │    years_since_last_promotion, years_with_current_manager         │
│   │    distance_from_home, business_travel                            │
│   │    overtime, environment_satisfaction                             │
│   │    job_satisfaction, relationship_satisfaction                    │
│   │    work_life_balance, performance_rating                          │
│   │    training_times_last_year, stock_option_level                   │
│   │    percent_salary_hike, attrition                                 │
│   │    hire_date, exit_date, is_active                                │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│   ┌──────────────────────┐              ┌──────────────────────────┐    │
│   │      dim_date         │              │  fact_performance_history │    │
│   ├──────────────────────┤              ├──────────────────────────┤    │
│   │ PK date_id           │              │ PK performance_id        │    │
│   │    full_date          │              │ FK employee_id           │    │
│   │    year, quarter      │              │    review_year           │    │
│   │    month, month_name  │              │    performance_rating    │    │
│   │    day, day_name      │              │    training_hours        │    │
│   │    is_weekend          │              │    projects_completed    │    │
│   └──────────────────────┘              │    review_date           │    │
│                                          └──────────────────────────┘    │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────┐        │
│   │                    audit_log                                │        │
│   ├────────────────────────────────────────────────────────────┤        │
│   │ PK audit_id                                                │        │
│   │    table_name, operation, record_id                        │        │
│   │    old_data (JSONB), new_data (JSONB)                      │        │
│   │    changed_by, changed_at                                  │        │
│   └────────────────────────────────────────────────────────────┘        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Entity Descriptions

### 3.1 fact_employee (Fact Table)
- **Type**: Fact table (transactional)
- **Rows**: ~5,000
- **Granularity**: One row per employee
- **Measures**: monthly_income, years_at_company, performance_rating, etc.
- **Dimensions**: Department, Job Role, Education, Location, Date

### 3.2 dim_department
- **Type**: Dimension table
- **Rows**: 10
- **Attributes**: department_name

### 3.3 dim_job_role
- **Type**: Dimension table (degenerate dimension)
- **Rows**: ~60
- **Attributes**: job_role_name
- **FK**: department_id

### 3.4 dim_education_level
- **Type**: Dimension table (outrigger)
- **Rows**: 5
- **Attributes**: education_level, description

### 3.5 dim_location
- **Type**: Dimension table
- **Rows**: ~50
- **Attributes**: city, state, country

### 3.6 dim_date
- **Type**: Date dimension
- **Rows**: ~9,855 (2000-2026)
- **Attributes**: Year, Quarter, Month, Day, Day Name, Weekend Flag

### 3.7 fact_performance_history
- **Type**: Accumulating snapshot fact
- **Rows**: ~15,000
- **Measures**: performance_rating, training_hours, projects_completed

### 3.8 audit_log
- **Type**: Audit table
- **Stores**: Change tracking for data governance

---

## 4. Relationships

| From | To | Type | Description |
|------|----|------|-------------|
| fact_employee | dim_department | Many-to-One | An employee belongs to one department |
| fact_employee | dim_job_role | Many-to-One | An employee has one job role |
| fact_employee | dim_education_level | Many-to-One | An employee has one education level |
| fact_employee | dim_location | Many-to-One | An employee works at one location |
| dim_job_role | dim_department | Many-to-One | A job role belongs to one department |
| fact_performance_history | fact_employee | Many-to-One | An employee has multiple performance reviews |

---

## 5. Constraints

### 5.1 Primary Keys
```sql
fact_employee:           employee_id (INTEGER)
dim_department:          department_id (SERIAL)
dim_job_role:            job_role_id (SERIAL)
dim_education_level:     education_level_id (SERIAL)
dim_location:            location_id (SERIAL)
dim_date:                date_id (SERIAL)
fact_performance_history: performance_id (SERIAL)
audit_log:               audit_id (SERIAL)
```

### 5.2 Foreign Keys
```sql
fact_employee.department_id             → dim_department.department_id
fact_employee.job_role_id               → dim_job_role.job_role_id
fact_employee.education_level_id        → dim_education_level.education_level_id
fact_employee.location_id               → dim_location.location_id
dim_job_role.department_id              → dim_department.department_id
fact_performance_history.employee_id    → fact_employee.employee_id
```

### 5.3 Check Constraints
```sql
age                                  BETWEEN 18 AND 80
monthly_income                       > 0
job_level                            BETWEEN 1 AND 5
satisfaction ratings                 BETWEEN 1 AND 4
performance_rating                   BETWEEN 1 AND 4
stock_option_level                   BETWEEN 0 AND 3
attrition                            IN ('Yes', 'No')
gender                               IN ('Male', 'Female')
marital_status                       IN ('Single', 'Married', 'Divorced')
overtime                             IN ('Yes', 'No')
business_travel                      IN ('Non-Travel', 'Travel_Rarely', 'Travel_Frequently')
exit_date                            >= hire_date (when not null)
```

---

## 6. Indexes

### 6.1 Single-Column Indexes
```sql
fact_employee:       department_id, job_role_id, education_level_id,
                     location_id, attrition, gender, hire_date,
                     exit_date, monthly_income, job_level,
                     performance_rating, job_satisfaction,
                     overtime, is_active
```

### 6.2 Composite Indexes
```sql
fact_employee:       (department_id, attrition)
fact_employee:       (department_id, gender)
fact_employee:       (department_id, monthly_income)
```

---

## 7. Sample Queries

### Query 1: Employee Count by Department
```sql
SELECT d.department_name, COUNT(*) AS employee_count
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY employee_count DESC;
```

### Query 2: Attrition Rate by Department
```sql
SELECT d.department_name,
       COUNT(*) AS total,
       SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
       ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY attrition_rate DESC;
```

### Query 3: Top 3 Salaries per Department (Window Function)
```sql
WITH ranked AS (
    SELECT d.department_name, f.employee_name, f.monthly_income,
           DENSE_RANK() OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS rank
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
)
SELECT * FROM ranked WHERE rank <= 3;
```
