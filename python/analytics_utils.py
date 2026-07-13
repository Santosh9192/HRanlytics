#!/usr/bin/env python3
"""
Analytics Utilities Module
===========================
Shared utility functions for HR analytics data processing.
Provides database connections, file I/O, common transformations,
and helper functions used across all Python modules.
"""

import pandas as pd
import numpy as np
import os
import json
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime

# Project root directory (two levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path constants
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_CLEANED_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
REPORTS_EXCEL_DIR = os.path.join(REPORTS_DIR, "excel")
REPORTS_HTML_DIR = os.path.join(REPORTS_DIR, "html")
REPORTS_PDF_DIR = os.path.join(REPORTS_DIR, "pdf")

# Ensure directories exist
for d in [DATA_CLEANED_DIR, DATA_PROCESSED_DIR, REPORTS_EXCEL_DIR,
          REPORTS_HTML_DIR, REPORTS_PDF_DIR]:
    os.makedirs(d, exist_ok=True)

# Column mapping for standardization
COLUMN_MAPPING = {
    "EmployeeID": "employee_id",
    "EmployeeName": "employee_name",
    "Age": "age",
    "Gender": "gender",
    "Department": "department",
    "JobRole": "job_role",
    "Education": "education",
    "EducationField": "education_field",
    "MaritalStatus": "marital_status",
    "MonthlyIncome": "monthly_income",
    "JobLevel": "job_level",
    "YearsAtCompany": "years_at_company",
    "YearsInCurrentRole": "years_in_current_role",
    "YearsSinceLastPromotion": "years_since_last_promotion",
    "YearsWithCurrentManager": "years_with_current_manager",
    "DistanceFromHome": "distance_from_home",
    "BusinessTravel": "business_travel",
    "OverTime": "overtime",
    "EnvironmentSatisfaction": "environment_satisfaction",
    "JobSatisfaction": "job_satisfaction",
    "RelationshipSatisfaction": "relationship_satisfaction",
    "WorkLifeBalance": "work_life_balance",
    "PerformanceRating": "performance_rating",
    "TrainingTimesLastYear": "training_times_last_year",
    "StockOptionLevel": "stock_option_level",
    "PercentSalaryHike": "percent_salary_hike",
    "Attrition": "attrition",
    "HireDate": "hire_date",
    "ExitDate": "exit_date",
    "City": "city",
    "State": "state",
    "Country": "country"
}

# Reverse mapping for output
REVERSE_COLUMN_MAPPING = {v: k for k, v in COLUMN_MAPPING.items()}

# Satisfaction level labels
SATISFACTION_LABELS = {
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Very High"
}

PERFORMANCE_LABELS = {
    1: "Below Average",
    2: "Average",
    3: "Good",
    4: "Excellent"
}

EDUCATION_LABELS = {
    1: "Below College",
    2: "College",
    3: "Bachelor's",
    4: "Master's",
    5: "Doctorate"
}

# KPI calculation functions
DEPARTMENT_ORDER = [
    "Sales", "Research & Development", "Human Resources", "Finance",
    "Information Technology", "Marketing", "Operations", "Customer Support",
    "Legal", "Administration"
]


def load_raw_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load raw HR dataset from CSV."""
    if file_path is None:
        file_path = os.path.join(DATA_RAW_DIR, "hr_data.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    print(f"Loading data from: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df):,} records with {len(df.columns)} columns.")
    return df


def load_cleaned_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load cleaned HR dataset."""
    if file_path is None:
        file_path = os.path.join(DATA_CLEANED_DIR, "hr_data_cleaned.csv")
    return pd.read_csv(file_path)


def save_cleaned_data(df: pd.DataFrame, filename: str = "hr_data_cleaned.csv") -> str:
    """Save cleaned dataset."""
    file_path = os.path.join(DATA_CLEANED_DIR, filename)
    df.to_csv(file_path, index=False)
    print(f"[SAVED] Cleaned data: {file_path}")
    return file_path


def save_processed_data(df: pd.DataFrame, filename: str) -> str:
    """Save processed/analysis results."""
    file_path = os.path.join(DATA_PROCESSED_DIR, filename)
    df.to_csv(file_path, index=False)
    print(f"[SAVED] Processed data: {file_path}")
    return file_path


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    rename_map = {col: COLUMN_MAPPING.get(col, col) for col in df.columns}
    return df.rename(columns=rename_map)


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate all key HR KPIs from employee data."""
    total = len(df)
    active = len(df[df["attrition"] == "No"])
    attrited = len(df[df["attrition"] == "Yes"])

    kpis = {
        "total_employees": total,
        "active_employees": active,
        "attrited_employees": attrited,
        "attrition_rate": round(attrited / total * 100, 2) if total > 0 else 0,
        "avg_salary": round(df["monthly_income"].mean(), 2),
        "median_salary": round(df["monthly_income"].median(), 2),
        "min_salary": round(df["monthly_income"].min(), 2),
        "max_salary": round(df["monthly_income"].max(), 2),
        "avg_age": round(df["age"].mean(), 1),
        "avg_tenure": round(df["years_at_company"].mean(), 1),
        "avg_job_satisfaction": round(df["job_satisfaction"].mean(), 2),
        "avg_work_life_balance": round(df["work_life_balance"].mean(), 2),
        "avg_performance_rating": round(df["performance_rating"].mean(), 2),
        "avg_years_since_promotion": round(df["years_since_last_promotion"].mean(), 2),
        "promotion_rate": round(
            len(df[df["years_since_last_promotion"] == 0]) / total * 100, 2
        ),
        "overtime_percentage": round(
            len(df[df["overtime"] == "Yes"]) / total * 100, 2
        ),
        "avg_training_hours": round(df["training_times_last_year"].mean(), 1),
        "male_count": int((df["gender"] == "Male").sum()),
        "female_count": int((df["gender"] == "Female").sum()),
        "female_percentage": round(
            (df["gender"] == "Female").sum() / total * 100, 2
        ),
        "department_count": df["department"].nunique(),
        "total_salary_budget": round(df["monthly_income"].sum(), 2),
        "calc_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return kpis


def get_age_group(age: int) -> str:
    """Categorize age into groups."""
    if age < 25:
        return "Under 25"
    elif age <= 34:
        return "25-34"
    elif age <= 44:
        return "35-44"
    elif age <= 54:
        return "45-54"
    else:
        return "55+"


def get_salary_range(income: float) -> str:
    """Categorize salary into ranges."""
    if income < 5000:
        return "Under $5K"
    elif income <= 7500:
        return "$5K-$7.5K"
    elif income <= 10000:
        return "$7.5K-$10K"
    elif income <= 15000:
        return "$10K-$15K"
    else:
        return "Above $15K"


def get_tenure_group(years: int) -> str:
    """Categorize tenure into groups."""
    if years < 2:
        return "0-1 Years"
    elif years <= 5:
        return "2-5 Years"
    elif years <= 10:
        return "6-10 Years"
    else:
        return "10+ Years"


def get_risk_category(row: pd.Series) -> str:
    """Calculate risk category based on multiple factors."""
    score = 0
    if row.get("job_satisfaction", 3) <= 2:
        score += 3
    if row.get("work_life_balance", 3) <= 2:
        score += 3
    if row.get("overtime", "No") == "Yes":
        score += 2
    if row.get("years_since_last_promotion", 0) > 3:
        score += 2
    if row.get("years_at_company", 5) < 2:
        score += 2

    if score >= 8:
        return "High Risk"
    elif score >= 4:
        return "Medium Risk"
    else:
        return "Low Risk"


def print_section(title: str, char: str = "=", width: int = 60):
    """Print a formatted section header."""
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


if __name__ == "__main__":
    # Test utility functions
    print_section("Testing Analytics Utilities")

    df = load_raw_data()
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    kpis = calculate_kpis(df)
    print(f"\nKey KPIs:")
    for k, v in kpis.items():
        print(f"  {k}: {v}")
