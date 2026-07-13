-- ============================================================
-- Window Functions & Advanced SQL Queries
-- ============================================================
-- Running totals, ranking functions, moving averages, lag/lead
-- ============================================================

-- 1. Employee Ranking by Salary within Department
SELECT
    d.department_name,
    f.employee_name,
    f.monthly_income,
    RANK() OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS salary_rank,
    DENSE_RANK() OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS dense_salary_rank,
    ROW_NUMBER() OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS row_num
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY d.department_name, salary_rank;

-- 2. Top 3 Highest Paid Employees per Department
WITH dept_salary_rank AS (
    SELECT
        d.department_name,
        f.employee_name,
        f.monthly_income,
        DENSE_RANK() OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS rank
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
)
SELECT *
FROM dept_salary_rank
WHERE rank <= 3
ORDER BY department_name, rank;

-- 3. Running Total of Hires by Year
SELECT
    EXTRACT(YEAR FROM hire_date)::INTEGER AS hire_year,
    COUNT(*) AS yearly_hires,
    SUM(COUNT(*)) OVER (ORDER BY EXTRACT(YEAR FROM hire_date)::INTEGER) AS running_total_hires
FROM fact_employee
GROUP BY hire_year
ORDER BY hire_year;

-- 4. Running Total of Attrition by Year
SELECT
    EXTRACT(YEAR FROM exit_date)::INTEGER AS exit_year,
    COUNT(*) AS yearly_attrition,
    SUM(COUNT(*)) OVER (ORDER BY EXTRACT(YEAR FROM exit_date)::INTEGER) AS running_total_attrition
FROM fact_employee
WHERE attrition = 'Yes' AND exit_date IS NOT NULL
GROUP BY exit_year
ORDER BY exit_year;

-- 5. Monthly Hire Trend with Moving Average (3-month)
SELECT
    EXTRACT(YEAR FROM hire_date)::INTEGER AS yr,
    EXTRACT(MONTH FROM hire_date)::INTEGER AS mon,
    COUNT(*) AS hires,
    AVG(COUNT(*)) OVER (ORDER BY EXTRACT(YEAR FROM hire_date), EXTRACT(MONTH FROM hire_date)
                         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3month
FROM fact_employee
GROUP BY yr, mon
ORDER BY yr, mon;

-- 6. Salary Percentile by Department
SELECT
    d.department_name,
    ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p25_salary,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p50_salary,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p75_salary,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS p90_salary
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY d.department_name;

-- 7. Salary Difference from Department Average
SELECT
    d.department_name,
    f.employee_name,
    f.monthly_income,
    ROUND(AVG(f.monthly_income) OVER (PARTITION BY f.department_id), 2) AS dept_avg_salary,
    ROUND(f.monthly_income - AVG(f.monthly_income) OVER (PARTITION BY f.department_id), 2) AS diff_from_avg
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY d.department_name, diff_from_avg DESC;

-- 8. Year-over-Year Hire Comparison
WITH yearly_hires AS (
    SELECT
        EXTRACT(YEAR FROM hire_date)::INTEGER AS yr,
        COUNT(*) AS hires
    FROM fact_employee
    GROUP BY yr
)
SELECT
    yr,
    hires,
    LAG(hires) OVER (ORDER BY yr) AS prev_year_hires,
    ROUND((hires - LAG(hires) OVER (ORDER BY yr)) * 100.0 / NULLIF(LAG(hires) OVER (ORDER BY yr), 0), 2) AS yoy_growth_pct
FROM yearly_hires
ORDER BY yr;

-- 9. Employee Tenure Ranking
SELECT
    employee_name,
    department_name,
    years_at_company,
    RANK() OVER (ORDER BY years_at_company DESC) AS tenure_rank,
    NTILE(4) OVER (ORDER BY years_at_company) AS tenure_quartile
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY tenure_rank
LIMIT 20;

-- 10. Department Salary Ranking with NTILE
SELECT
    d.department_name,
    f.employee_name,
    f.monthly_income,
    NTILE(4) OVER (PARTITION BY f.department_id ORDER BY f.monthly_income) AS salary_quartile
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY d.department_name, f.monthly_income;

-- 11. First and Last Employee Hired per Department
WITH dept_hires AS (
    SELECT
        d.department_name,
        f.employee_name,
        f.hire_date,
        FIRST_VALUE(f.employee_name) OVER (PARTITION BY f.department_id ORDER BY f.hire_date) AS first_hired,
        LAST_VALUE(f.employee_name) OVER (PARTITION BY f.department_id ORDER BY f.hire_date
            RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_hired
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
)
SELECT DISTINCT department_name, first_hired, last_hired
FROM dept_hires;

-- 12. Cumulative Salary Cost by Department
SELECT
    d.department_name,
    f.employee_name,
    f.monthly_income,
    SUM(f.monthly_income) OVER (PARTITION BY f.department_id ORDER BY f.employee_name) AS running_salary_cost
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY d.department_name, f.employee_name;

-- 13. Salary Lead/Lag Analysis (Compare with next rank)
SELECT
    d.department_name,
    f.employee_name,
    f.monthly_income,
    LEAD(f.monthly_income) OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS next_lower_salary,
    LAG(f.monthly_income) OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC) AS next_higher_salary,
    ROUND(f.monthly_income - LEAD(f.monthly_income) OVER (PARTITION BY f.department_id ORDER BY f.monthly_income DESC), 2) AS gap_to_next
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY d.department_name, f.monthly_income DESC;

-- 14. Attrition Rate by Department (Window Function Version)
SELECT DISTINCT
    d.department_name,
    COUNT(*) OVER (PARTITION BY f.department_id) AS total_employees,
    SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) OVER (PARTITION BY f.department_id) AS attrited,
    ROUND(
        SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) OVER (PARTITION BY f.department_id) * 100.0 /
        COUNT(*) OVER (PARTITION BY f.department_id), 2
    ) AS attrition_rate
FROM fact_employee f
JOIN dim_department d ON f.department_id = d.department_id
ORDER BY attrition_rate DESC;

-- 15. Experience Band Distribution with Running Total
SELECT
    CASE
        WHEN years_at_company < 2 THEN '0-1 Years'
        WHEN years_at_company BETWEEN 2 AND 5 THEN '2-5 Years'
        WHEN years_at_company BETWEEN 6 AND 10 THEN '6-10 Years'
        ELSE '10+ Years'
    END AS experience_band,
    COUNT(*) AS employee_count,
    SUM(COUNT(*)) OVER (ORDER BY MIN(years_at_company)) AS running_total
FROM fact_employee
GROUP BY experience_band
ORDER BY MIN(years_at_company);
