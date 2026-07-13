-- ============================================================
-- Stored Procedures for HR Analytics
-- ============================================================
-- Automated data maintenance, reporting, and analysis procedures
-- ============================================================

-- SP1: Refresh Employee Status (Update is_active)
CREATE OR REPLACE PROCEDURE sp_refresh_employee_status()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE fact_employee
    SET is_active = CASE WHEN attrition = 'No' THEN TRUE ELSE FALSE END,
        updated_at = CURRENT_TIMESTAMP
    WHERE is_active IS DISTINCT FROM (CASE WHEN attrition = 'No' THEN TRUE ELSE FALSE END);

    RAISE NOTICE 'Employee status refreshed successfully.';
END;
$$;

-- SP2: Calculate and Update Attrition Rate by Department
CREATE OR REPLACE PROCEDURE sp_calculate_dept_attrition(
    OUT dept_name VARCHAR,
    OUT attrition_rate NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS temp_dept_attrition AS
    SELECT
        d.department_name,
        ROUND(SUM(CASE WHEN f.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rate
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
    GROUP BY d.department_name
    ORDER BY rate DESC;

    SELECT department_name, rate INTO dept_name, attrition_rate
    FROM temp_dept_attrition
    LIMIT 1;
END;
$$;

-- SP3: Generate Department Salary Report
CREATE OR REPLACE PROCEDURE sp_department_salary_report(
    IN p_department_id INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_department_id IS NULL THEN
        -- Report for all departments
        SELECT
            d.department_name,
            COUNT(*) AS employee_count,
            ROUND(MIN(f.monthly_income), 2) AS min_salary,
            ROUND(AVG(f.monthly_income), 2) AS avg_salary,
            ROUND(MAX(f.monthly_income), 2) AS max_salary,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS median_salary,
            ROUND(STDDEV(f.monthly_income), 2) AS salary_std_dev,
            ROUND(SUM(f.monthly_income), 2) AS total_monthly_cost
        FROM fact_employee f
        JOIN dim_department d ON f.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY d.department_name;
    ELSE
        -- Report for specific department
        SELECT
            d.department_name,
            COUNT(*) AS employee_count,
            ROUND(MIN(f.monthly_income), 2) AS min_salary,
            ROUND(AVG(f.monthly_income), 2) AS avg_salary,
            ROUND(MAX(f.monthly_income), 2) AS max_salary,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.monthly_income), 2) AS median_salary,
            ROUND(STDDEV(f.monthly_income), 2) AS salary_std_dev,
            ROUND(SUM(f.monthly_income), 2) AS total_monthly_cost
        FROM fact_employee f
        JOIN dim_department d ON f.department_id = d.department_id
        WHERE f.department_id = p_department_id
        GROUP BY d.department_name;
    END IF;
END;
$$;

-- SP4: Identify High-Risk Attrition Employees
CREATE OR REPLACE PROCEDURE sp_attrition_risk_assessment()
LANGUAGE plpgsql
RETURNS TABLE (
    employee_id INTEGER,
    employee_name VARCHAR,
    department_name VARCHAR(100),
    risk_score NUMERIC,
    risk_category VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        f.employee_id,
        f.employee_name,
        d.department_name,
        ROUND(
            (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
            (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
            (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
            (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
            (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END),
        0) AS risk_score,
        CASE
            WHEN (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
                 (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
                 (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
                 (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
                 (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END) >= 8
            THEN 'High Risk'
            WHEN (CASE WHEN f.job_satisfaction <= 2 THEN 3 ELSE 0 END) +
                 (CASE WHEN f.work_life_balance <= 2 THEN 3 ELSE 0 END) +
                 (CASE WHEN f.overtime = 'Yes' THEN 2 ELSE 0 END) +
                 (CASE WHEN f.years_since_last_promotion > 3 THEN 2 ELSE 0 END) +
                 (CASE WHEN f.years_at_company < 2 THEN 2 ELSE 0 END) >= 4
            THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS risk_category
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
    WHERE f.attrition = 'No'
    ORDER BY risk_score DESC;
END;
$$ LANGUAGE plpgsql;

-- SP5: Monthly KPI Snapshot
CREATE OR REPLACE PROCEDURE sp_monthly_kpi_snapshot(
    IN p_year INTEGER,
    IN p_month INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        COUNT(*) AS total_employees,
        SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_employees,
        ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate,
        ROUND(AVG(monthly_income), 2) AS avg_salary,
        ROUND(AVG(age), 1) AS avg_age,
        ROUND(AVG(years_at_company), 1) AS avg_tenure,
        ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
        ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance,
        ROUND(AVG(performance_rating), 2) AS avg_performance,
        SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS overtime_pct,
        SUM(CASE WHEN years_since_last_promotion = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promotion_rate
    FROM fact_employee;

    RAISE NOTICE 'Monthly KPI snapshot generated for %-%', p_year, p_month;
END;
$$;

-- SP6: Employee Promotion Eligibility Check
CREATE OR REPLACE PROCEDURE sp_promotion_eligible()
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        f.employee_id,
        f.employee_name,
        d.department_name,
        jr.job_role_name,
        f.job_level,
        f.performance_rating,
        f.years_in_current_role,
        f.years_since_last_promotion,
        CASE
            WHEN f.performance_rating >= 3 AND f.years_in_current_role >= 2 THEN 'Eligible'
            WHEN f.performance_rating >= 3 AND f.years_in_current_role >= 1 THEN 'Consider'
            ELSE 'Not Eligible'
        END AS eligibility_status
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
    JOIN dim_job_role jr ON f.job_role_id = jr.job_role_id
    WHERE f.attrition = 'No'
    ORDER BY eligibility_status, f.performance_rating DESC;
END;
$$;

-- SP7: Update Employee Data
CREATE OR REPLACE PROCEDURE sp_update_employee_salary(
    IN p_employee_id INTEGER,
    IN p_new_salary NUMERIC(10,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Audit the change
    INSERT INTO audit_log (table_name, operation, record_id, old_data, new_data)
    VALUES (
        'fact_employee',
        'SALARY_UPDATE',
        p_employee_id,
        jsonb_build_object('monthly_income', (SELECT monthly_income FROM fact_employee WHERE employee_id = p_employee_id)),
        jsonb_build_object('monthly_income', p_new_salary)
    );

    -- Update the salary
    UPDATE fact_employee
    SET monthly_income = p_new_salary,
        updated_at = CURRENT_TIMESTAMP
    WHERE employee_id = p_employee_id;

    RAISE NOTICE 'Employee % salary updated to %', p_employee_id, p_new_salary;
END;
$$;

-- SP8: Department Headcount Report
CREATE OR REPLACE PROCEDURE sp_headcount_report(
    IN p_date DATE DEFAULT CURRENT_DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        d.department_name,
        COUNT(*) AS total_headcount,
        SUM(CASE WHEN f.hire_date <= p_date AND (f.exit_date IS NULL OR f.exit_date > p_date) THEN 1 ELSE 0 END) AS active_headcount,
        SUM(CASE WHEN f.hire_date > p_date - INTERVAL '30 days' AND f.hire_date <= p_date THEN 1 ELSE 0 END) AS new_hires_30d,
        SUM(CASE WHEN f.exit_date > p_date - INTERVAL '30 days' AND f.exit_date <= p_date THEN 1 ELSE 0 END) AS exits_30d
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
    GROUP BY d.department_name
    ORDER BY active_headcount DESC;
END;
$$;

-- SP9: Data Quality Check
CREATE OR REPLACE PROCEDURE sp_data_quality_check()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check for missing exit dates on attrited employees
    SELECT 'Missing Exit Date' AS issue, COUNT(*) AS count
    FROM fact_employee
    WHERE attrition = 'Yes' AND exit_date IS NULL

    UNION ALL

    -- Check for negative values
    SELECT 'Negative Years', COUNT(*)
    FROM fact_employee
    WHERE years_at_company < 0 OR years_in_current_role < 0

    UNION ALL

    -- Check for invalid ages
    SELECT 'Invalid Age', COUNT(*)
    FROM fact_employee
    WHERE age < 18 OR age > 80

    UNION ALL

    -- Check for orphaned records
    SELECT 'Missing Department', COUNT(*)
    FROM fact_employee f
    LEFT JOIN dim_department d ON f.department_id = d.department_id
    WHERE d.department_id IS NULL

    UNION ALL

    -- Check duplicate employee IDs
    SELECT 'Duplicate IDs', COUNT(*) - COUNT(DISTINCT employee_id)
    FROM fact_employee

    UNION ALL

    -- Check invalid salary values
    SELECT 'Invalid Salary', COUNT(*)
    FROM fact_employee
    WHERE monthly_income <= 0;
END;
$$;

-- SP10: Generate Yearly Attrition Report
CREATE OR REPLACE PROCEDURE sp_yearly_attrition_report(
    IN p_year INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        d.department_name,
        COUNT(*) AS starting_headcount,
        SUM(CASE WHEN EXTRACT(YEAR FROM f.exit_date) = p_year THEN 1 ELSE 0 END) AS attrited,
        ROUND(SUM(CASE WHEN EXTRACT(YEAR FROM f.exit_date) = p_year THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS attrition_rate,
        ROUND(AVG(CASE WHEN EXTRACT(YEAR FROM f.exit_date) = p_year THEN f.years_at_company END), 1) AS avg_tenure_at_exit,
        ROUND(AVG(CASE WHEN EXTRACT(YEAR FROM f.exit_date) = p_year THEN f.age END), 1) AS avg_age_at_exit
    FROM fact_employee f
    JOIN dim_department d ON f.department_id = d.department_id
    WHERE EXTRACT(YEAR FROM f.hire_date) <= p_year
      AND (f.exit_date IS NULL OR EXTRACT(YEAR FROM f.exit_date) >= p_year)
    GROUP BY d.department_name
    ORDER BY attrition_rate DESC;

    RAISE NOTICE 'Yearly attrition report generated for %', p_year;
END;
$$;
