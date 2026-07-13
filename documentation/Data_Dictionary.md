# Data Dictionary

## HR Analytics Dataset

---

## Overview

This document defines all fields in the HR Analytics dataset, including data types, valid values, descriptions, and business rules.

---

## Employee Table (fact_employee)

| # | Column Name | Data Type | Length | Required | Description | Valid Values |
|---|-------------|-----------|--------|----------|-------------|-------------|
| 1 | employee_id | INTEGER | — | Yes | Unique identifier for each employee | 1001-6000 |
| 2 | employee_name | VARCHAR | 200 | Yes | Full name of employee | — |
| 3 | age | INTEGER | — | Yes | Age of the employee in years | 18-80 |
| 4 | gender | VARCHAR | 10 | Yes | Gender identity | 'Male', 'Female' |
| 5 | department | VARCHAR | 100 | Yes | Department name | See Department Dimension |
| 6 | job_role | VARCHAR | 100 | Yes | Job title/role | See Job Role Dimension |
| 7 | education | INTEGER | — | Yes | Education level code | 1-5 |
| 8 | education_field | VARCHAR | 100 | Yes | Field of highest education | See Education Fields |
| 9 | marital_status | VARCHAR | 20 | Yes | Marital status | 'Single', 'Married', 'Divorced' |
| 10 | monthly_income | NUMERIC | 10,2 | Yes | Monthly salary in USD | 3,000 - 25,000+ |
| 11 | job_level | INTEGER | — | Yes | Job seniority level | 1 (Entry) to 5 (Executive) |
| 12 | years_at_company | INTEGER | — | Yes | Total years employed | 0+ |
| 13 | years_in_current_role | INTEGER | — | Yes | Years in current position | 0+ |
| 14 | years_since_last_promotion | INTEGER | — | Yes | Years since last promotion | 0+ |
| 15 | years_with_current_manager | INTEGER | — | Yes | Years with current supervisor | 0+ |
| 16 | distance_from_home | INTEGER | — | Yes | Commute distance in miles | 1-50 |
| 17 | business_travel | VARCHAR | 50 | Yes | Frequency of business travel | See Travel Options |
| 18 | overtime | VARCHAR | 5 | Yes | Whether employee works overtime | 'Yes', 'No' |
| 19 | environment_satisfaction | INTEGER | — | Yes | Satisfaction with work environment | 1 (Low) to 4 (Very High) |
| 20 | job_satisfaction | INTEGER | — | Yes | Satisfaction with job | 1 (Low) to 4 (Very High) |
| 21 | relationship_satisfaction | INTEGER | — | Yes | Satisfaction with relationships | 1 (Low) to 4 (Very High) |
| 22 | work_life_balance | INTEGER | — | Yes | Work-life balance rating | 1 (Bad) to 4 (Good) |
| 23 | performance_rating | INTEGER | — | Yes | Annual performance rating | 1 (Below Avg) to 4 (Excellent) |
| 24 | training_times_last_year | INTEGER | — | Yes | Number of trainings attended | 0-6 |
| 25 | stock_option_level | INTEGER | — | Yes | Stock option level | 0 (None) to 3 (High) |
| 26 | percent_salary_hike | NUMERIC | 5,1 | Yes | Percentage salary increase | 8.0 - 25.0% |
| 27 | attrition | VARCHAR | 5 | Yes | Whether employee has left | 'Yes', 'No' |
| 28 | hire_date | DATE | — | Yes | Date of hire | 2000-01-01 to 2024-12-31 |
| 29 | exit_date | DATE | — | No | Date of exit (if applicable) | ≥ hire_date |
| 30 | city | VARCHAR | 100 | Yes | City of employment | US Cities |
| 31 | state | VARCHAR | 50 | Yes | State of employment | US State Codes |
| 32 | country | VARCHAR | 50 | Yes | Country | 'United States' |

---

## Dimension Tables

### Department Dimension (dim_department)

| Department ID | Department Name | Average Employees |
|--------------|-----------------|------------------|
| 1 | Sales | ~600 |
| 2 | Research & Development | ~900 |
| 3 | Human Resources | ~300 |
| 4 | Finance | ~400 |
| 5 | Information Technology | ~750 |
| 6 | Marketing | ~500 |
| 7 | Operations | ~400 |
| 8 | Customer Support | ~600 |
| 9 | Legal | ~250 |
| 10 | Administration | ~300 |

### Education Level Dimension (dim_education_level)

| Level ID | Level Name | Description |
|----------|------------|-------------|
| 1 | Below College | High school diploma or equivalent |
| 2 | College | Associate degree or some college |
| 3 | Bachelor's Degree | 4-year university degree |
| 4 | Master's Degree | Graduate degree |
| 5 | Doctorate Degree | PhD or equivalent |

### Job Level Dimension

| Level | Title | Typical Salary Range |
|-------|-------|---------------------|
| 1 | Entry Level | $3,000 - $6,000 |
| 2 | Junior | $5,000 - $9,000 |
| 3 | Mid Level | $7,000 - $13,000 |
| 4 | Senior | $10,000 - $18,000 |
| 5 | Executive | $15,000 - $25,000 |

### Satisfaction/Performance Scale

| Rating | Label | Meaning |
|--------|-------|---------|
| 1 | Low / Below Average | Needs significant improvement |
| 2 | Medium / Average | Meets minimum expectations |
| 3 | High / Good | Exceeds expectations |
| 4 | Very High / Excellent | Outstanding performance |

---

## Categorical Code Values

### Business Travel Options
| Value | Description |
|-------|-------------|
| Non-Travel | Does not travel for business |
| Travel_Rarely | Travels occasionally (1-2 times/year) |
| Travel_Frequently | Travels regularly (monthly+) |

### Education Fields
| Field | Typical Departments |
|-------|-------------------|
| Life Sciences | R&D, Healthcare |
| Medical | R&D, Healthcare |
| Marketing | Sales, Marketing |
| Technical Degree | IT, Engineering |
| Human Resources | HR, Administration |
| Business Management | All departments |
| Engineering | IT, Operations |
| Computer Science | IT |
| Finance | Finance |
| Law | Legal |
| Arts | Marketing |
| Other | Various |

### Marital Status
| Value | Description |
|-------|-------------|
| Single | Not married |
| Married | Currently married |
| Divorced | Legally divorced |

### Overtime
| Value | Description |
|-------|-------------|
| Yes | Regularly works overtime |
| No | Does not work overtime |

---

## Derived Fields

| Field | Formula | Description |
|-------|---------|-------------|
| Age Group | CASE WHEN age < 25 THEN 'Under 25' ... | Categorized age ranges |
| Salary Range | CASE WHEN income < 5000 THEN 'Under $5K' ... | Categorized income bands |
| Tenure Group | CASE WHEN years < 2 THEN '0-1 Years' ... | Categorized tenure |
| Satisfaction Score | AVG of 4 satisfaction metrics | Composite satisfaction |
| Performance Score | Rating * 0.5 + Training * 0.3 + Hike * 0.2 | Performance composite |
| Risk Score | Sum of weighted risk factors | Attrition risk assessment |
| Risk Category | CASE WHEN score >= 8 THEN 'High Risk' | Risk classification |

---

## Data Quality Rules

| Rule | Constraint | Action |
|------|-----------|--------|
| Age Range | 18 ≤ age ≤ 80 | Flag for review |
| Salary | > 0 | Reject record |
| Satisfaction | 1 ≤ value ≤ 4 | Cap at boundaries |
| Hire Date | ≤ current date | Flag future dates |
| Exit Date | ≥ Hire Date | Correct relationship |
| Attrition Logic | 'Yes' → has exit date | Flag inconsistency |
| Employee ID | Unique | Deduplicate |
