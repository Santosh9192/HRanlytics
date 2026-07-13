-- ============================================================
-- Salary Analysis Queries
-- ============================================================
-- Compensation analysis, salary distribution, pay equity
-- ============================================================

-- 1. Overall Salary Statistics
SELECT
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income), 2) AS median_salary,
    MIN(monthly_income) AS min_salary,
    MAX(monthly_income) AS max_salary,
    ROUND(STDDEV(monthly_income), 2) AS std_dev_salary
FROM fact_employee;

-- 2. Average Salary by Department
SELECT
    d.department_name,
    COUNT(*) AS employees,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS median_salary,
    ROUND(MIN(f.monthly_income), 2) AS min_salary,
    ROUND(MAX(f.monthly_income), 2) AS max_salary
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_salary DESC;

-- 3. Average Salary by Job Level
SELECT
    job_level,
    COUNT(*) AS employees,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income), 2) AS median_salary
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 4. Average Salary by Education Level
SELECT
    e.education_level,
    COUNT(*) AS employees,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(AVG(f.percent_salary_hike), 2) AS avg_hike
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level
ORDER BY e.education_level;

-- 5. Average Salary by Gender (Pay Equity Check)
SELECT
    gender,
    COUNT(*) AS employees,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(MIN(monthly_income), 2) AS min_salary,
    ROUND(MAX(monthly_income), 2) AS max_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income), 2) AS median_salary
FROM fact_employee
GROUP BY gender;

-- 6. Gender Pay Gap by Department
SELECT
    d.department_name,
    ROUND(AVG(CASE WHEN f.gender = 'Male' THEN f.monthly_income END), 2) AS male_avg_salary,
    ROUND(AVG(CASE WHEN f.gender = 'Female' THEN f.monthly_income END), 2) AS female_avg_salary,
    ROUND(
        AVG(CASE WHEN f.gender = 'Male' THEN f.monthly_income END) -
        AVG(CASE WHEN f.gender = 'Female' THEN f.monthly_income END)
    , 2) AS pay_gap,
    ROUND(
        (AVG(CASE WHEN f.gender = 'Male' THEN f.monthly_income END) -
         AVG(CASE WHEN f.gender = 'Female' THEN f.monthly_income END)) /
        NULLIF(AVG(CASE WHEN f.gender = 'Male' THEN f.monthly_income END), 0) * 100
    , 2) AS pay_gap_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY pay_gap_pct DESC;

-- 7. Salary Distribution by Job Role (Top Paying)
SELECT
    jr.job_role_name,
    d.department_name,
    COUNT(*) AS employees,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(MIN(f.monthly_income), 2) AS min_salary,
    ROUND(MAX(f.monthly_income), 2) AS max_salary
FROM fact_employee f
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
JOIN dim_department d ON jr.department_id = d.department_id
GROUP BY jr.job_role_name, d.department_name
ORDER BY avg_salary DESC
LIMIT 15;

-- 8. Salary Hike Analysis
SELECT
    CASE
        WHEN percent_salary_hike < 10 THEN 'Below 10%'
        WHEN percent_salary_hike BETWEEN 10 AND 14 THEN '10-14%'
        WHEN percent_salary_hike BETWEEN 15 AND 19 THEN '15-19%'
        ELSE '20%+'
    END AS hike_range,
    COUNT(*) AS employees,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(performance_rating), 2) AS avg_performance
FROM fact_employee
GROUP BY hike_range
ORDER BY MIN(percent_salary_hike);

-- 9. Salary vs Performance Rating
SELECT
    performance_rating,
    COUNT(*) AS employees,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(percent_salary_hike), 2) AS avg_hike_pct,
    ROUND(MIN(monthly_income), 2) AS min_salary,
    ROUND(MAX(monthly_income), 2) AS max_salary
FROM fact_employee
GROUP BY performance_rating
ORDER BY performance_rating;

-- 10. Salary by Experience (Years at Company)
SELECT
    CASE
        WHEN years_at_company < 2 THEN '0-1 Years'
        WHEN years_at_company BETWEEN 2 AND 5 THEN '2-5 Years'
        WHEN years_at_company BETWEEN 6 AND 10 THEN '6-10 Years'
        ELSE '10+ Years'
    END AS tenure_group,
    COUNT(*) AS employees,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(percent_salary_hike), 2) AS avg_hike
FROM fact_employee
GROUP BY tenure_group
ORDER BY MIN(years_at_company);

-- 11. Top 10 Highest Paid Employees
SELECT
    employee_name,
    department_name,
    job_role_name,
    monthly_income,
    job_level,
    years_at_company
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
ORDER BY monthly_income DESC
LIMIT 10;

-- 12. Salary Range by Department
SELECT
    d.department_name,
    ROUND(MIN(f.monthly_income), 2) AS min_salary,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(MAX(f.monthly_income), 2) AS max_salary,
    ROUND(MAX(f.monthly_income) - MIN(f.monthly_income), 2) AS salary_span
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY salary_span DESC;

-- 13. Salary by Education and Job Level
SELECT
    e.education_level,
    f.job_level,
    COUNT(*) AS employees,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level, f.job_level
ORDER BY e.education_level, f.job_level;

-- 14. Compensation to Income Ratio by Department
SELECT
    d.department_name,
    ROUND(AVG(f.monthly_income) / NULLIF(AVG(f.years_at_company + 1), 0), 2) AS comp_to_tenure_ratio,
    ROUND(AVG(f.percent_salary_hike), 2) AS avg_hike_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY comp_to_tenure_ratio DESC;

-- 15. Active Employees with Below-Average Salary
SELECT
    COUNT(*) AS below_avg_count,
    ROUND(AVG(monthly_income), 2) AS their_avg_salary,
    ROUND((SELECT AVG(monthly_income) FROM fact_employee WHERE attrition = 'No'), 2) AS company_avg
FROM fact_employee
WHERE attrition = 'No'
  AND monthly_income < (SELECT AVG(monthly_income) FROM fact_employee WHERE attrition = 'No');
