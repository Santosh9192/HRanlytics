-- ============================================================
-- Promotion Analysis Queries
-- ============================================================
-- Promotion trends, promotion gap analysis, career progression
-- ============================================================

-- 1. Overall Promotion Statistics
SELECT
    ROUND(AVG(years_since_last_promotion), 2) AS avg_years_since_promotion,
    MAX(years_since_last_promotion) AS max_years_since_promotion,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted_current_year,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promotion_rate
FROM fact_employee;

-- 2. Promotion Rate by Department
SELECT
    d.department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN f.years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted_this_year,
    ROUND(SUM(CASE WHEN f.years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate,
    ROUND(AVG(f.years_since_last_promotion), 2) AS avg_years_since_promotion
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY promotion_rate DESC;

-- 3. Promotion Rate by Job Level
SELECT
    job_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted_this_year,
    ROUND(SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate,
    ROUND(AVG(years_since_last_promotion), 2) AS avg_years_since_promotion
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 4. Employees Overdue for Promotion (3+ years since last promotion)
SELECT
    d.department_name,
    COUNT(*) AS overdue_count,
    ROUND(AVG(f.years_since_last_promotion), 1) AS avg_years_overdue,
    ROUND(AVG(f.performance_rating), 2) AS avg_performance
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
WHERE f.years_since_last_promotion >= 3
  AND f.attrition = 'No'
GROUP BY d.department_name
ORDER BY overdue_count DESC;

-- 5. Promotion History Distribution
SELECT
    years_since_last_promotion,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY years_since_last_promotion
ORDER BY years_since_last_promotion;

-- 6. Promotion Rate by Performance Rating
SELECT
    performance_rating,
    COUNT(*) AS total,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted,
    ROUND(SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate
FROM fact_employee
GROUP BY performance_rating
ORDER BY performance_rating;

-- 7. Promotion Rate by Gender
SELECT
    gender,
    COUNT(*) AS total,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted,
    ROUND(SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate
FROM fact_employee
GROUP BY gender;

-- 8. Promotion Rate by Education Level
SELECT
    e.education_level,
    COUNT(*) AS total,
    SUM(CASE WHEN f.years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted,
    ROUND(SUM(CASE WHEN f.years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level
ORDER BY e.education_level;

-- 9. Average Years Between Promotions by Department
SELECT
    d.department_name,
    ROUND(AVG(f.years_since_last_promotion), 2) AS avg_promotion_cycle,
    COUNT(*) AS employee_count
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
WHERE f.years_at_company > 0
GROUP BY d.department_name
ORDER BY avg_promotion_cycle;

-- 10. Job Level Distribution (Career Progression)
SELECT
    d.department_name,
    ROUND(AVG(CASE WHEN f.job_level = 1 THEN 100.0 ELSE 0 END), 1) AS pct_level_1,
    ROUND(AVG(CASE WHEN f.job_level = 2 THEN 100.0 ELSE 0 END), 1) AS pct_level_2,
    ROUND(AVG(CASE WHEN f.job_level = 3 THEN 100.0 ELSE 0 END), 1) AS pct_level_3,
    ROUND(AVG(CASE WHEN f.job_level = 4 THEN 100.0 ELSE 0 END), 1) AS pct_level_4,
    ROUND(AVG(CASE WHEN f.job_level = 5 THEN 100.0 ELSE 0 END), 1) AS pct_level_5
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY d.department_name;

-- 11. Promotion Rate by Age Group
SELECT
    CASE
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS total,
    SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) AS promoted,
    ROUND(SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate
FROM fact_employee
GROUP BY age_group
ORDER BY MIN(age);

-- 12. Promotion vs Attrition Correlation
SELECT
    CASE
        WHEN years_since_last_promotion <= 1 THEN 'Recent/On-time'
        WHEN years_since_last_promotion BETWEEN 2 AND 3 THEN 'Moderate delay'
        ELSE 'Long delay'
    END AS promotion_status,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY promotion_status
ORDER BY MIN(years_since_last_promotion);

-- 13. Employees Ready for Promotion (High Performers in same role 2+ years)
SELECT
    f.employee_name,
    jr.job_role_name,
    d.department_name,
    f.performance_rating,
    f.years_in_current_role,
    f.years_since_last_promotion
FROM fact_employee f
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
JOIN dim_department d ON jr.department_id = d.department_id
WHERE f.performance_rating >= 3
  AND f.years_in_current_role >= 2
  AND f.attrition = 'No'
ORDER BY f.performance_rating DESC, f.years_in_current_role DESC;

-- 14. High Performers Not Promoted (Potential flight risks)
SELECT
    f.employee_name,
    d.department_name,
    jr.job_role_name,
    f.performance_rating,
    f.years_since_last_promotion,
    f.monthly_income
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
WHERE f.performance_rating = 4
  AND f.years_since_last_promotion >= 3
  AND f.attrition = 'No'
ORDER BY f.years_since_last_promotion DESC;

-- 15. Promotion Rate Trend by Year (using hire date as proxy)
SELECT
    EXTRACT(YEAR FROM hire_date)::INTEGER AS hire_year,
    COUNT(*) AS hired,
    ROUND(AVG(years_since_last_promotion), 2) AS avg_years_to_promotion,
    SUM(CASE WHEN years_since_last_promotion <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS quick_promotion_pct
FROM fact_employee
GROUP BY hire_year
ORDER BY hire_year;
