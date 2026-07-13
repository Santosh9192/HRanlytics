-- ============================================================
-- HR Analytics Database Schema
-- ============================================================
-- Database: hr_analytics
-- Description: Normalized PostgreSQL database for HR analytics
-- ============================================================

-- Create Database (run separately if needed)
-- CREATE DATABASE hr_analytics;

-- ─── 1. Department Dimension ───
CREATE TABLE IF NOT EXISTS dim_department (
    department_id    SERIAL PRIMARY KEY,
    department_name  VARCHAR(100) NOT NULL UNIQUE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── 2. Education Level Dimension ───
CREATE TABLE IF NOT EXISTS dim_education_level (
    education_level_id  SERIAL PRIMARY KEY,
    education_level    VARCHAR(50) NOT NULL UNIQUE,
    description        VARCHAR(200)
);

-- ─── 3. Job Role Dimension ───
CREATE TABLE IF NOT EXISTS dim_job_role (
    job_role_id    SERIAL PRIMARY KEY,
    job_role_name  VARCHAR(100) NOT NULL UNIQUE,
    department_id  INTEGER REFERENCES dim_department(department_id),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── 4. Location Dimension ───
CREATE TABLE IF NOT EXISTS dim_location (
    location_id  SERIAL PRIMARY KEY,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(50) NOT NULL,
    country      VARCHAR(50) DEFAULT 'United States',
    UNIQUE(city, state, country)
);

-- ─── 5. Date Dimension ───
CREATE TABLE IF NOT EXISTS dim_date (
    date_id       SERIAL PRIMARY KEY,
    full_date     DATE NOT NULL UNIQUE,
    year          INTEGER NOT NULL,
    quarter       INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month         INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    month_name    VARCHAR(20) NOT NULL,
    day           INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_name      VARCHAR(20) NOT NULL,
    is_weekend    BOOLEAN DEFAULT FALSE
);

-- ─── 6. Employee Fact Table ───
CREATE TABLE IF NOT EXISTS fact_employee (
    employee_id              INTEGER PRIMARY KEY,
    employee_name            VARCHAR(200) NOT NULL,
    age                      INTEGER NOT NULL CHECK (age BETWEEN 18 AND 80),
    gender                   VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    department_id            INTEGER NOT NULL REFERENCES dim_department(department_id),
    job_role_id              INTEGER NOT NULL REFERENCES dim_job_role(job_role_id),
    education_level_id       INTEGER NOT NULL REFERENCES dim_education_level(education_level_id),
    education_field          VARCHAR(100),
    marital_status           VARCHAR(20) CHECK (marital_status IN ('Single', 'Married', 'Divorced')),
    monthly_income           NUMERIC(10,2) NOT NULL CHECK (monthly_income > 0),
    job_level                INTEGER NOT NULL CHECK (job_level BETWEEN 1 AND 5),
    years_at_company         INTEGER NOT NULL DEFAULT 0,
    years_in_current_role    INTEGER NOT NULL DEFAULT 0,
    years_since_last_promotion INTEGER NOT NULL DEFAULT 0,
    years_with_current_manager INTEGER NOT NULL DEFAULT 0,
    distance_from_home       INTEGER NOT NULL DEFAULT 0,
    business_travel          VARCHAR(50) CHECK (business_travel IN ('Non-Travel', 'Travel_Rarely', 'Travel_Frequently')),
    overtime                 VARCHAR(5) CHECK (overtime IN ('Yes', 'No')),
    environment_satisfaction INTEGER CHECK (environment_satisfaction BETWEEN 1 AND 4),
    job_satisfaction         INTEGER CHECK (job_satisfaction BETWEEN 1 AND 4),
    relationship_satisfaction INTEGER CHECK (relationship_satisfaction BETWEEN 1 AND 4),
    work_life_balance        INTEGER CHECK (work_life_balance BETWEEN 1 AND 4),
    performance_rating       INTEGER CHECK (performance_rating BETWEEN 1 AND 4),
    training_times_last_year INTEGER DEFAULT 0,
    stock_option_level       INTEGER DEFAULT 0 CHECK (stock_option_level BETWEEN 0 AND 3),
    percent_salary_hike      NUMERIC(5,1) DEFAULT 0,
    attrition                VARCHAR(5) NOT NULL CHECK (attrition IN ('Yes', 'No')),
    hire_date                DATE NOT NULL,
    exit_date                DATE,
    location_id              INTEGER REFERENCES dim_location(location_id),
    is_active                BOOLEAN GENERATED ALWAYS AS (CASE WHEN attrition = 'No' THEN TRUE ELSE FALSE END) STORED,
    created_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_dates CHECK (exit_date IS NULL OR exit_date >= hire_date),
    CONSTRAINT valid_age_at_hire CHECK (age >= (EXTRACT(YEAR FROM hire_date) - (EXTRACT(YEAR FROM CURRENT_DATE) - age)))
);

-- ─── Indexes ───
CREATE INDEX idx_fact_employee_department ON fact_employee(department_id);
CREATE INDEX idx_fact_employee_job_role ON fact_employee(job_role_id);
CREATE INDEX idx_fact_employee_education ON fact_employee(education_level_id);
CREATE INDEX idx_fact_employee_location ON fact_employee(location_id);
CREATE INDEX idx_fact_employee_attrition ON fact_employee(attrition);
CREATE INDEX idx_fact_employee_gender ON fact_employee(gender);
CREATE INDEX idx_fact_employee_hire_date ON fact_employee(hire_date);
CREATE INDEX idx_fact_employee_exit_date ON fact_employee(exit_date);
CREATE INDEX idx_fact_employee_monthly_income ON fact_employee(monthly_income);
CREATE INDEX idx_fact_employee_job_level ON fact_employee(job_level);
CREATE INDEX idx_fact_employee_performance ON fact_employee(performance_rating);
CREATE INDEX idx_fact_employee_satisfaction ON fact_employee(job_satisfaction);
CREATE INDEX idx_fact_employee_overtime ON fact_employee(overtime);
CREATE INDEX idx_fact_employee_is_active ON fact_employee(is_active);

-- ─── Composite indexes for common queries ───
CREATE INDEX idx_fact_employee_dept_attrition ON fact_employee(department_id, attrition);
CREATE INDEX idx_fact_employee_dept_gender ON fact_employee(department_id, gender);
CREATE INDEX idx_fact_employee_dept_income ON fact_employee(department_id, monthly_income);

-- ─── Audit Log Table ───
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id       SERIAL PRIMARY KEY,
    table_name     VARCHAR(100) NOT NULL,
    operation      VARCHAR(10) NOT NULL,
    record_id      INTEGER,
    old_data       JSONB,
    new_data       JSONB,
    changed_by     VARCHAR(100) DEFAULT CURRENT_USER,
    changed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── Employee Performance History ───
CREATE TABLE IF NOT EXISTS fact_performance_history (
    performance_id   SERIAL PRIMARY KEY,
    employee_id      INTEGER NOT NULL REFERENCES fact_employee(employee_id),
    review_year      INTEGER NOT NULL,
    performance_rating INTEGER CHECK (performance_rating BETWEEN 1 AND 4),
    training_hours   INTEGER DEFAULT 0,
    projects_completed INTEGER DEFAULT 0,
    review_date      DATE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, review_year)
);

CREATE INDEX idx_perf_emp_year ON fact_performance_history(employee_id, review_year);
