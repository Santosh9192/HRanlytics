-- ============================================================
-- Data Insert Scripts
-- ============================================================
-- This script loads dimension and fact tables from CSV data.
-- ============================================================

-- ─── 1. Load Department Dimension ───
INSERT INTO dim_department (department_name) VALUES
    ('Sales'),
    ('Research & Development'),
    ('Human Resources'),
    ('Finance'),
    ('Information Technology'),
    ('Marketing'),
    ('Operations'),
    ('Customer Support'),
    ('Legal'),
    ('Administration')
ON CONFLICT (department_name) DO NOTHING;

-- ─── 2. Load Education Level Dimension ───
INSERT INTO dim_education_level (education_level, description) VALUES
    (1, 'Below College'),
    (2, 'College'),
    (3, 'Bachelor''s Degree'),
    (4, 'Master''s Degree'),
    (5, 'Doctorate Degree')
ON CONFLICT (education_level) DO NOTHING;

-- ─── 3. Load Job Roles ───
INSERT INTO dim_job_role (job_role_name, department_id)
SELECT jr.role_name, d.department_id
FROM (VALUES
    ('Sales', 'Sales Executive'),
    ('Sales', 'Sales Representative'),
    ('Sales', 'Sales Manager'),
    ('Sales', 'Sales Development Rep'),
    ('Sales', 'Account Executive'),
    ('Sales', 'Regional Sales Director'),
    ('Research & Development', 'Research Scientist'),
    ('Research & Development', 'Laboratory Technician'),
    ('Research & Development', 'Research Director'),
    ('Research & Development', 'Clinical Research Coordinator'),
    ('Research & Development', 'R&D Manager'),
    ('Research & Development', 'Product Developer'),
    ('Human Resources', 'HR Executive'),
    ('Human Resources', 'HR Manager'),
    ('Human Resources', 'HR Coordinator'),
    ('Human Resources', 'Talent Acquisition Specialist'),
    ('Human Resources', 'Compensation Analyst'),
    ('Human Resources', 'HR Director'),
    ('Finance', 'Accountant'),
    ('Finance', 'Financial Analyst'),
    ('Finance', 'Finance Manager'),
    ('Finance', 'Auditor'),
    ('Finance', 'Financial Controller'),
    ('Finance', 'CFO'),
    ('Information Technology', 'Software Engineer'),
    ('Information Technology', 'Data Analyst'),
    ('Information Technology', 'IT Manager'),
    ('Information Technology', 'DevOps Engineer'),
    ('Information Technology', 'Systems Administrator'),
    ('Information Technology', 'CTO'),
    ('Marketing', 'Marketing Executive'),
    ('Marketing', 'Marketing Manager'),
    ('Marketing', 'Content Writer'),
    ('Marketing', 'Digital Marketing Specialist'),
    ('Marketing', 'Brand Manager'),
    ('Marketing', 'Marketing Director'),
    ('Operations', 'Operations Analyst'),
    ('Operations', 'Operations Manager'),
    ('Operations', 'Supply Chain Coordinator'),
    ('Operations', 'Logistics Specialist'),
    ('Operations', 'Facilities Manager'),
    ('Operations', 'COO'),
    ('Customer Support', 'Customer Support Rep'),
    ('Customer Support', 'Support Manager'),
    ('Customer Support', 'Customer Success Manager'),
    ('Customer Support', 'Technical Support Engineer'),
    ('Customer Support', 'Quality Assurance Specialist'),
    ('Customer Support', 'Support Director'),
    ('Legal', 'Legal Advisor'),
    ('Legal', 'Corporate Counsel'),
    ('Legal', 'Compliance Officer'),
    ('Legal', 'Legal Secretary'),
    ('Legal', 'Paralegal'),
    ('Legal', 'General Counsel'),
    ('Administration', 'Administrative Assistant'),
    ('Administration', 'Office Manager'),
    ('Administration', 'Executive Assistant'),
    ('Administration', 'Receptionist'),
    ('Administration', 'Administration Director'),
    ('Administration', 'Facilities Coordinator')
) AS jr(dept_name, role_name)
JOIN dim_department d ON d.department_name = jr.dept_name
ON CONFLICT (job_role_name) DO NOTHING;

-- ─── 4. Load Date Dimension ───
INSERT INTO dim_date (full_date, year, quarter, month, month_name, day, day_name, is_weekend)
SELECT
    d::DATE,
    EXTRACT(YEAR FROM d)::INTEGER,
    EXTRACT(QUARTER FROM d)::INTEGER,
    EXTRACT(MONTH FROM d)::INTEGER,
    TO_CHAR(d, 'Month')::VARCHAR(20),
    EXTRACT(DAY FROM d)::INTEGER,
    TO_CHAR(d, 'Day')::VARCHAR(20),
    CASE WHEN EXTRACT(DOW FROM d) IN (0, 6) THEN TRUE ELSE FALSE END
FROM generate_series('2000-01-01'::DATE, '2026-12-31'::DATE, '1 day'::INTERVAL) AS d
ON CONFLICT (full_date) DO NOTHING;

-- ─── 5. Load Locations from CSV ───
INSERT INTO dim_location (city, state, country)
SELECT DISTINCT city, state, 'United States'
FROM temp_hr_import
ON CONFLICT (city, state, country) DO NOTHING;

-- ─── 6. Main Data Import from CSV ───
-- Create a temporary staging table for CSV import
CREATE TEMP TABLE temp_hr_import (
    employee_id              INTEGER,
    employee_name            VARCHAR(200),
    age                      INTEGER,
    gender                   VARCHAR(10),
    department               VARCHAR(100),
    job_role                 VARCHAR(100),
    education                INTEGER,
    education_field          VARCHAR(100),
    marital_status           VARCHAR(20),
    monthly_income           NUMERIC(10,2),
    job_level                INTEGER,
    years_at_company         INTEGER,
    years_in_current_role    INTEGER,
    years_since_last_promotion INTEGER,
    years_with_current_manager INTEGER,
    distance_from_home       INTEGER,
    business_travel          VARCHAR(50),
    overtime                 VARCHAR(5),
    environment_satisfaction INTEGER,
    job_satisfaction         INTEGER,
    relationship_satisfaction INTEGER,
    work_life_balance        INTEGER,
    performance_rating       INTEGER,
    training_times_last_year INTEGER,
    stock_option_level       INTEGER,
    percent_salary_hike      NUMERIC(5,1),
    attrition                VARCHAR(5),
    hire_date                DATE,
    exit_date                DATE,
    city                     VARCHAR(100),
    state                    VARCHAR(50),
    country                  VARCHAR(50)
);

-- Import CSV data (adjust path as needed)
-- COPY temp_hr_import FROM 'D:/sbcmdcode/Data Analyst/HRanalyst/data/raw/hr_data.csv'
-- WITH (FORMAT CSV, HEADER true, DELIMITER ',');

-- Or use \copy in psql:
-- \copy temp_hr_import FROM 'D:/sbcmdcode/Data Analyst/HRanalyst/data/raw/hr_data.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

-- Insert into fact_employee
INSERT INTO fact_employee (
    employee_id, employee_name, age, gender, department_id, job_role_id,
    education_level_id, education_field, marital_status, monthly_income,
    job_level, years_at_company, years_in_current_role, years_since_last_promotion,
    years_with_current_manager, distance_from_home, business_travel, overtime,
    environment_satisfaction, job_satisfaction, relationship_satisfaction,
    work_life_balance, performance_rating, training_times_last_year,
    stock_option_level, percent_salary_hike, attrition, hire_date, exit_date, location_id
)
SELECT
    t.employee_id, t.employee_name, t.age, t.gender,
    d.department_id, jr.job_role_id,
    t.education, t.education_field, t.marital_status, t.monthly_income,
    t.job_level, t.years_at_company, t.years_in_current_role,
    t.years_since_last_promotion, t.years_with_current_manager,
    t.distance_from_home, t.business_travel, t.overtime,
    t.environment_satisfaction, t.job_satisfaction, t.relationship_satisfaction,
    t.work_life_balance, t.performance_rating, t.training_times_last_year,
    t.stock_option_level, t.percent_salary_hike, t.attrition,
    t.hire_date,
    NULLIF(t.exit_date, '')::DATE,
    l.location_id
FROM temp_hr_import t
JOIN dim_department d ON d.department_name = t.department
JOIN dim_job_role jr ON jr.job_role_name = t.job_role
JOIN dim_location l ON l.city = t.city AND l.state = t.state
ON CONFLICT (employee_id) DO NOTHING;

-- Insert performance history records (synthetic data)
INSERT INTO fact_performance_history (employee_id, review_year, performance_rating, training_hours, projects_completed)
SELECT
    employee_id,
    EXTRACT(YEAR FROM hire_date)::INTEGER + yr_offset AS review_year,
    CASE
        WHEN performance_rating = 4 THEN 4
        WHEN performance_rating = 3 THEN GREATEST(2, performance_rating - (yr_offset % 2))
        ELSE GREATEST(1, performance_rating)
    END AS performance_rating,
    training_times_last_year * 4 + (yr_offset * 2) AS training_hours,
    GREATEST(1, yr_offset * 3 + (yr_offset % 2)) AS projects_completed
FROM fact_employee
CROSS JOIN LATERAL (
    SELECT generate_series(0, GREATEST(0, LEAST(3, years_at_company - 1))) AS yr_offset
) yr
WHERE EXTRACT(YEAR FROM hire_date)::INTEGER + yr_offset <= 2026;

-- Clean up temp table
DROP TABLE IF EXISTS temp_hr_import;

-- Verify data loaded
SELECT 'Departments:' AS check_type, COUNT(*) AS count FROM dim_department
UNION ALL
SELECT 'Job Roles:', COUNT(*) FROM dim_job_role
UNION ALL
SELECT 'Employees:', COUNT(*) FROM fact_employee
UNION ALL
SELECT 'Active Employees:', COUNT(*) FROM fact_employee WHERE is_active = TRUE;
