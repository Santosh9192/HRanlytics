-- ============================================================
-- Attrition Analysis Queries
-- ============================================================
-- Deep dive into employee attrition patterns, trends, and drivers
-- ============================================================

-- 1. Overall Attrition Rate
SELECT
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee;

-- 2. Attrition Rate by Department
SELECT
    d.department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY attrition_rate DESC;

-- 3. Attrition by Age Group
SELECT
    CASE
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate
FROM fact_employee
GROUP BY age_group
ORDER BY MIN(age);

-- 4. Attrition by Gender
SELECT
    gender,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY gender;

-- 5. Attrition by Job Level
SELECT
    job_level,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 6. Attrition by Marital Status
SELECT
    marital_status,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY marital_status
ORDER BY attrition_rate DESC;

-- 7. Attrition by Salary Range
SELECT
    CASE
        WHEN monthly_income < 5000 THEN 'Under $5K'
        WHEN monthly_income BETWEEN 5000 AND 7500 THEN '$5K-$7.5K'
        WHEN monthly_income BETWEEN 7501 AND 10000 THEN '$7.5K-$10K'
        WHEN monthly_income BETWEEN 10001 AND 15000 THEN '$10K-$15K'
        ELSE 'Above $15K'
    END AS salary_range,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate
FROM fact_employee
GROUP BY salary_range
ORDER BY MIN(monthly_income);

-- 8. Attrition by Years at Company
SELECT
    CASE
        WHEN years_at_company < 2 THEN '0-1 Years'
        WHEN years_at_company BETWEEN 2 AND 5 THEN '2-5 Years'
        WHEN years_at_company BETWEEN 6 AND 10 THEN '6-10 Years'
        ELSE '10+ Years'
    END AS tenure_group,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate
FROM fact_employee
GROUP BY tenure_group
ORDER BY MIN(years_at_company);

-- 9. Attrition by Overtime
SELECT
    overtime,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY overtime;

-- 10. Attrition by Job Satisfaction Level
SELECT
    job_satisfaction,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY job_satisfaction
ORDER BY job_satisfaction;

-- 11. Attrition by Work-Life Balance
SELECT
    work_life_balance,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY work_life_balance
ORDER BY work_life_balance;

-- 12. Attrition by Performance Rating
SELECT
    performance_rating,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY performance_rating
ORDER BY performance_rating;

-- 13. Attrition by Business Travel
SELECT
    business_travel,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY business_travel
ORDER BY attrition_rate DESC;

-- 14. Attrition by Education Level
SELECT
    e.education_level,
    COUNT(*) AS total,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level
ORDER BY e.education_level;

-- 15. Attrition by Department and Gender (Drill-down)
SELECT
    d.department_name,
    f.gender,
    COUNT(*) AS total,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name, f.gender
ORDER BY d.department_name, f.gender;

-- 16. Attrition Analysis by Years Since Last Promotion
SELECT
    CASE
        WHEN years_since_last_promotion = 0 THEN 'Promoted this year'
        WHEN years_since_last_promotion BETWEEN 1 AND 2 THEN '1-2 years ago'
        WHEN years_since_last_promotion BETWEEN 3 AND 5 THEN '3-5 years ago'
        ELSE '5+ years ago'
    END AS promotion_status,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate
FROM fact_employee
GROUP BY promotion_status
ORDER BY MIN(years_since_last_promotion);

-- 17. Monthly Attrition Trend
SELECT
    EXTRACT(YEAR FROM exit_date)::INTEGER AS exit_year,
    EXTRACT(MONTH FROM exit_date)::INTEGER AS exit_month,
    COUNT(*) AS monthly_attrition
FROM fact_employee
WHERE attrition = 'Yes' AND exit_date IS NOT NULL
GROUP BY exit_year, exit_month
ORDER BY exit_year, exit_month;

-- 18. Attrition Rate by Job Role (Top 10 Highest)
SELECT
    jr.job_role_name,
    d.department_name,
    COUNT(*) AS total,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee f
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
JOIN dim_department d ON jr.department_id = d.department_id
GROUP BY jr.job_role_name, d.department_name
HAVING COUNT(*) >= 10
ORDER BY attrition_rate DESC
LIMIT 10;

-- 19. Average Salary Difference: Attrited vs Active
SELECT
    attrition,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(percent_salary_hike), 2) AS avg_hike_pct,
    ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM fact_employee
GROUP BY attrition;

-- 20. Attrition Risk Score (Multi-factor)
SELECT
    employee_id,
    employee_name,
    department_name,
    job_role_name,
    job_satisfaction,
    work_life_balance,
    overtime,
    years_since_last_promotion,
    ROUND(
        (CASE WHEN job_satisfaction <= 2 THEN 3 ELSE 0 END) +
        (CASE WHEN work_life_balance <= 2 THEN 3 ELSE 0 END) +
        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
        (CASE WHEN years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
        (CASE WHEN years_at_company < 2 THEN 2 ELSE 0 END)
    , 0) AS risk_score
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
WHERE f.attrition = 'No'
ORDER BY risk_score DESC, employee_name
LIMIT 20;
