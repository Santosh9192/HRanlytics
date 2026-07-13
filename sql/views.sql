-- ============================================================
-- Database Views for HR Analytics
-- ============================================================
-- Reusable views for common analytical queries
-- ============================================================

-- V1: Employee Details View (Comprehensive)
CREATE OR REPLACE VIEW v_employee_details AS
SELECT
    f.employee_id,
    f.employee_name,
    f.age,
    f.gender,
    d.department_name,
    jr.job_role_name,
    el.education_level,
    f.education_field,
    f.marital_status,
    f.monthly_income,
    f.job_level,
    f.years_at_company,
    f.years_in_current_role,
    f.years_since_last_promotion,
    f.years_with_current_manager,
    f.distance_from_home,
    f.business_travel,
    f.overtime,
    f.environment_satisfaction,
    f.job_satisfaction,
    f.relationship_satisfaction,
    f.work_life_balance,
    f.performance_rating,
    f.training_times_last_year,
    f.stock_option_level,
    f.percent_salary_hike,
    f.attrition,
    f.hire_date,
    f.exit_date,
    f.is_active,
    l.city,
    l.state,
    l.country
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
JOIN dim_education_level el ON f.education_level_id = el.education_level_id
JOIN dim_location l ON f.location_id = l.location_id;

-- V2: Department Summary View
CREATE OR REPLACE VIEW v_department_summary AS
SELECT
    d.department_id,
    d.department_name,
    COUNT(f.employee_id) AS total_employees,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited_count,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(AVG(f.age), 1) AS avg_age,
    ROUND(AVG(f.years_at_company), 1) AS avg_tenure,
    ROUND(AVG(f.performance_rating), 2) AS avg_performance,
    ROUND(AVG(f.job_satisfaction), 2) AS avg_job_satisfaction,
    SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) AS female_count,
    SUM(CASE WHEN f.overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_count
FROM dim_department d
LEFT JOIN fact_employee f ON d.department_id = f.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_name;

-- V3: Attrition Analysis View
CREATE OR REPLACE VIEW v_attrition_analysis AS
SELECT
    f.employee_id,
    f.employee_name,
    f.age,
    f.gender,
    d.department_name,
    jr.job_role_name,
    f.monthly_income,
    f.job_level,
    f.years_at_company,
    f.years_since_last_promotion,
    f.overtime,
    f.job_satisfaction,
    f.work_life_balance,
    f.performance_rating,
    f.business_travel,
    f.marital_status,
    f.training_times_last_year,
    f.hire_date,
    f.exit_date,
    CASE
        WHEN f.exit_date IS NOT NULL THEN
            EXTRACT(YEAR FROM AGE(f.exit_date, f.hire_date)) * 12 +
            EXTRACT(MONTH FROM AGE(f.exit_date, f.hire_date))
        ELSE NULL
    END AS tenure_months
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
WHERE f.attrition = 'Yes';

-- V4: Salary Distribution View
CREATE OR REPLACE VIEW v_salary_distribution AS
SELECT
    d.department_name,
    jr.job_role_name,
    f.job_level,
    COUNT(*) AS employee_count,
    ROUND(MIN(f.monthly_income), 2) AS min_salary,
    ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p25_salary,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS median_salary,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p75_salary,
    ROUND(MAX(f.monthly_income), 2) AS max_salary,
    ROUND(STDDEV(f.monthly_income), 2) AS std_dev_salary
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
GROUP BY d.department_name, jr.job_role_name, f.job_level
ORDER BY d.department_name, avg_salary DESC;

-- V5: Performance Overview View
CREATE OR REPLACE VIEW v_performance_overview AS
SELECT
    f.employee_id,
    f.employee_name,
    d.department_name,
    jr.job_role_name,
    f.performance_rating,
    CASE
        WHEN f.performance_rating = 4 THEN 'Excellent'
        WHEN f.performance_rating = 3 THEN 'Good'
        WHEN f.performance_rating = 2 THEN 'Average'
        ELSE 'Below Average'
    END AS performance_label,
    f.job_satisfaction,
    f.work_life_balance,
    f.training_times_last_year,
    f.percent_salary_hike,
    f.years_since_last_promotion,
    f.overtime
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id;

-- V6: Diversity Dashboard View
CREATE OR REPLACE VIEW v_diversity_dashboard AS
SELECT
    d.department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) AS female,
    SUM(CASE WHEN f.gender = 'Male' THEN 1 ELSE 0 END) AS male,
    ROUND(SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS female_pct,
    ROUND(AVG(f.age), 1) AS avg_age,
    COUNT(DISTINCT f.education_field) AS education_diversity,
    COUNT(DISTINCT f.marital_status) AS marital_diversity
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name;

-- V7: Employee Tenure View
CREATE OR REPLACE VIEW v_employee_tenure AS
SELECT
    f.employee_id,
    f.employee_name,
    d.department_name,
    jr.job_role_name,
    f.years_at_company,
    f.years_in_current_role,
    f.years_since_last_promotion,
    f.years_with_current_manager,
    CASE
        WHEN f.years_at_company < 2 THEN 'New Hire'
        WHEN f.years_at_company BETWEEN 2 AND 5 THEN 'Short Term'
        WHEN f.years_at_company BETWEEN 6 AND 10 THEN 'Mid Term'
        ELSE 'Long Term'
    END AS tenure_category,
    CASE
        WHEN f.years_since_last_promotion >= 3 THEN 'Overdue'
        ELSE 'On Track'
    END AS promotion_status
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id;

-- V8: Monthly Headcount Trend View
CREATE OR REPLACE VIEW v_monthly_headcount AS
SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(DISTINCT f.employee_id) AS headcount,
    COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM f.hire_date) = dd.year
                        AND EXTRACT(MONTH FROM f.hire_date) = dd.month
                   THEN f.employee_id END) AS new_hires,
    COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM f.exit_date) = dd.year
                        AND EXTRACT(MONTH FROM f.exit_date) = dd.month
                   THEN f.employee_id END) AS exits
FROM dim_date dd
CROSS JOIN fact_employee f
WHERE dd.full_date BETWEEN '2023-01-01' AND '2026-12-31'
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;

-- V9: Training Analysis View
CREATE OR REPLACE VIEW v_training_analysis AS
SELECT
    d.department_name,
    ROUND(AVG(f.training_times_last_year), 2) AS avg_training_count,
    ROUND(SUM(f.training_times_last_year) * 1.0 / COUNT(*), 2) AS training_per_employee,
    ROUND(AVG(f.performance_rating), 2) AS avg_performance,
    ROUND(AVG(f.percent_salary_hike), 2) AS avg_salary_hike,
    COUNT(*) AS employee_count
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_training_count DESC;

-- V10: Employee Risk Assessment View
CREATE OR REPLACE VIEW v_employee_risk_assessment AS
SELECT
    f.employee_id,
    f.employee_name,
    d.department_name,
    jr.job_role_name,
    f.attrition,
    f.job_satisfaction,
    f.work_life_balance,
    f.overtime,
    f.years_since_last_promotion,
    f.performance_rating,
    f.monthly_income,
    ROUND(
        (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
        (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
        (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
        (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
        (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END) +
        (CASE WHEN f.performance_rating <= 2 THEN 2 ELSE 0 END)
    , 0) AS risk_score,
    CASE
        WHEN (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
             (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
             (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
             (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
             (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END) +
             (CASE WHEN f.performance_rating <= 2 THEN 2 ELSE 0 END) >= 8
        THEN 'High Risk'
        WHEN (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
             (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
             (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
             (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
             (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END) +
             (CASE WHEN f.performance_rating <= 2 THEN 2 ELSE 0 END) >= 4
        THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id;
