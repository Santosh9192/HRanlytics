-- ============================================================
-- Employee Analysis Queries
-- ============================================================
-- Total headcount, demographics, department distribution, etc.
-- ============================================================

-- 1. Total Employee Count
SELECT 'Total Employees' AS metric, COUNT(*) AS value FROM fact_employee;

-- 2. Active vs Attrited Employee Count
SELECT
    attrition,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY attrition;

-- 3. Employee Count by Department
SELECT
    d.department_name,
    COUNT(*) AS employee_count,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary,
    ROUND(AVG(f.age), 1) AS avg_age
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY employee_count DESC;

-- 4. Employee Count by Gender
SELECT
    gender,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY gender;

-- 5. Employee Count by Age Group
SELECT
    CASE
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
GROUP BY age_group
ORDER BY MIN(age);

-- 6. Employee Count by Education Level
SELECT
    e.education_level,
    COUNT(*) AS employee_count,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level
ORDER BY e.education_level;

-- 7. Employee Count by Job Level
SELECT
    job_level,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 8. Employee Count by Marital Status
SELECT
    marital_status,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
GROUP BY marital_status;

-- 9. Employee Distribution by Job Role (Top 15)
SELECT
    jr.job_role_name,
    d.department_name,
    COUNT(*) AS employee_count,
    ROUND(AVG(f.monthly_income), 2) AS avg_salary
FROM fact_employee f
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
JOIN dim_department d ON jr.department_id = d.department_id
GROUP BY jr.job_role_name, d.department_name
ORDER BY employee_count DESC
LIMIT 15;

-- 10. Gender Distribution by Department
SELECT
    d.department_name,
    SUM(CASE WHEN f.gender = 'Male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) AS female_count,
    ROUND(SUM(CASE WHEN f.gender = 'Male' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS male_pct,
    ROUND(SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS female_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY d.department_name;

-- 11. Average Age by Department
SELECT
    d.department_name,
    COUNT(*) AS employee_count,
    ROUND(AVG(f.age), 1) AS avg_age,
    MIN(f.age) AS min_age,
    MAX(f.age) AS max_age
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_age DESC;

-- 12. Employees by Generation
SELECT
    CASE
        WHEN age BETWEEN 18 AND 27 THEN 'Gen Z'
        WHEN age BETWEEN 28 AND 43 THEN 'Millennials'
        WHEN age BETWEEN 44 AND 59 THEN 'Gen X'
        ELSE 'Baby Boomers'
    END AS generation,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM fact_employee
GROUP BY generation
ORDER BY MIN(age);

-- 13. Employee Count by Business Travel Frequency
SELECT
    business_travel,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY business_travel
ORDER BY employee_count DESC;

-- 14. Average Distance from Home by Department
SELECT
    d.department_name,
    COUNT(*) AS employee_count,
    ROUND(AVG(f.distance_from_home), 1) AS avg_distance,
    MAX(f.distance_from_home) AS max_distance
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_distance DESC;

-- 15. Employee Count by City (Top 20)
SELECT
    l.city,
    l.state,
    COUNT(*) AS employee_count
FROM fact_employee f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY l.city, l.state
ORDER BY employee_count DESC
LIMIT 20;

-- 16. Stock Option Level Distribution
SELECT
    stock_option_level,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
GROUP BY stock_option_level
ORDER BY stock_option_level;

-- 17. Overtime Distribution by Department
SELECT
    d.department_name,
    SUM(CASE WHEN f.overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_yes,
    SUM(CASE WHEN f.overtime = 'No' THEN 1 ELSE 0 END) AS overtime_no,
    ROUND(SUM(CASE WHEN f.overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY overtime_pct DESC;

-- 18. Job Hopping Risk: Employees with short tenure
SELECT
    COUNT(*) AS short_tenure_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_employee), 2) AS percentage
FROM fact_employee
WHERE years_at_company < 2;

-- 19. Employees by Hire Year Trend
SELECT
    EXTRACT(YEAR FROM hire_date)::INTEGER AS hire_year,
    COUNT(*) AS hired_count,
    ROUND(AVG(monthly_income), 2) AS avg_starting_salary
FROM fact_employee
GROUP BY hire_year
ORDER BY hire_year;

-- 20. Top 10 Longest Tenured Employees
SELECT
    employee_name,
    department_name,
    job_role_name,
    years_at_company,
    age,
    monthly_income
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
ORDER BY years_at_company DESC
LIMIT 10;
