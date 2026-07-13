-- ============================================================
-- Overtime Analysis Queries
-- ============================================================
-- Overtime patterns, impact on attrition, performance, satisfaction
-- ============================================================

-- 1. Overall Overtime Statistics
SELECT
    overtime,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY overtime;

-- 2. Overtime by Department
SELECT
    d.department_name,
    COUNT(*) AS total,
    SUM(CASE WHEN f.overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_yes,
    ROUND(SUM(CASE WHEN f.overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY overtime_pct DESC;

-- 3. Overtime Impact on Attrition
SELECT
    overtime,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate
FROM fact_employee
GROUP BY overtime;

-- 4. Overtime by Job Level
SELECT
    job_level,
    COUNT(*) AS total,
    SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_yes,
    ROUND(SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_pct
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 5. Overtime vs Performance Rating
SELECT
    overtime,
    ROUND(AVG(performance_rating), 2) AS avg_performance,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance
FROM fact_employee
GROUP BY overtime;

-- 6. Overtime by Gender
SELECT
    gender,
    COUNT(*) AS total,
    SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_yes,
    ROUND(SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_pct
FROM fact_employee
GROUP BY gender;

-- 7. Overtime by Marital Status
SELECT
    marital_status,
    COUNT(*) AS total,
    SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_yes,
    ROUND(SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_pct
FROM fact_employee
GROUP BY marital_status
ORDER BY overtime_pct DESC;

-- 8. Overtime Impact on Satisfaction
SELECT
    overtime,
    ROUND(AVG(environment_satisfaction), 2) AS avg_env_satisfaction,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(relationship_satisfaction), 2) AS avg_relationship_satisfaction,
    ROUND(AVG(work_life_balance), 2) AS avg_wlb
FROM fact_employee
GROUP BY overtime;

-- 9. Departments with Highest Overtime and Attrition Correlation
SELECT
    d.department_name,
    ROUND(AVG(CASE WHEN f.overtime = 'Yes' THEN 1.0 ELSE 0 END) * 100, 2) AS overtime_pct,
    ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate,
    COUNT(*) AS total
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY overtime_pct DESC;

-- 10. Overtime Employees with Low Satisfaction (Risk Group)
SELECT
    COUNT(*) AS at_risk_count,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
WHERE overtime = 'Yes'
  AND job_satisfaction <= 2
  AND work_life_balance <= 2
  AND attrition = 'No';
