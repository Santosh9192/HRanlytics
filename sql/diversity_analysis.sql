-- ============================================================
-- Diversity & Inclusion Analysis Queries
-- ============================================================
-- Gender diversity, age diversity, education diversity
-- ============================================================

-- 1. Overall Gender Diversity
SELECT
    gender,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY gender;

-- 2. Gender Diversity by Department
SELECT
    d.department_name,
    COUNT(*) AS total,
    SUM(CASE WHEN f.gender = 'Male' THEN 1 ELSE 0 END) AS male,
    SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) AS female,
    ROUND(SUM(CASE WHEN f.gender = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS female_pct,
    ROUND(SUM(CASE WHEN f.gender = 'Male' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS male_pct
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY female_pct DESC;

-- 3. Gender Diversity by Job Level
SELECT
    job_level,
    COUNT(*) AS total,
    SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) AS male,
    SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) AS female,
    ROUND(SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS female_pct
FROM fact_employee
GROUP BY job_level
ORDER BY job_level;

-- 4. Age Diversity Distribution
SELECT
    CASE
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage,
    ROUND(AVG(monthly_income), 2) AS avg_salary
FROM fact_employee
GROUP BY age_group
ORDER BY MIN(age);

-- 5. Age Diversity by Department
SELECT
    d.department_name,
    ROUND(AVG(f.age), 1) AS avg_age,
    MIN(f.age) AS youngest,
    MAX(f.age) AS oldest,
    ROUND(STDDEV(f.age), 1) AS age_std_dev
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_age DESC;

-- 6. Education Diversity
SELECT
    e.education_level,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee f
JOIN dim_education_level e ON f.education_level_id = e.education_level_id
GROUP BY e.education_level
ORDER BY e.education_level;

-- 7. Education Field Distribution
SELECT
    education_field,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_employee
GROUP BY education_field
ORDER BY employee_count DESC;

-- 8. Education Field by Gender
SELECT
    education_field,
    SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) AS male,
    SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) AS female,
    COUNT(*) AS total,
    ROUND(SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS female_pct
FROM fact_employee
GROUP BY education_field
ORDER BY total DESC;

-- 9. Marital Status Diversity by Department
SELECT
    d.department_name,
    SUM(CASE WHEN f.marital_status = 'Single' THEN 1 ELSE 0 END) AS single,
    SUM(CASE WHEN f.marital_status = 'Married' THEN 1 ELSE 0 END) AS married,
    SUM(CASE WHEN f.marital_status = 'Divorced' THEN 1 ELSE 0 END) AS divorced,
    COUNT(*) AS total
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY d.department_name;

-- 10. Diversity Score by Department (Composite)
SELECT
    d.department_name,
    COUNT(*) AS total,
    ROUND(
        (COUNT(DISTINCT CASE WHEN f.gender = 'Female' THEN 1 ELSE NULL END) +
         COUNT(DISTINCT CASE WHEN f.age < 30 THEN 1 ELSE NULL END) +
         COUNT(DISTINCT CASE WHEN f.age > 50 THEN 1 ELSE NULL END)) * 100.0 / 3
    , 2) AS diversity_score
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY diversity_score DESC;
