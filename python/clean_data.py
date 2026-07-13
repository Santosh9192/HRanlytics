#!/usr/bin/env python3
"""
Data Cleaning Module
=====================
Cleans raw HR data by handling missing values, removing duplicates,
correcting data types, and flagging outliers.

Pipeline:
  load_raw() -> handle_missing_values() -> remove_duplicates()
  -> correct_data_types() -> handle_outliers() -> save_cleaned()
"""

import pandas as pd
import numpy as np
import os
import sys
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics_utils import (
    load_raw_data, save_cleaned_data, standardize_columns,
    DATA_RAW_DIR, DATA_CLEANED_DIR, print_section
)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    Strategy:
      - Numeric columns: fill with median
      - Categorical columns: fill with mode
      - Drop rows with critical missing values (employee_id, attrition)
    """
    print("\nHandling missing values...")
    initial_nulls = df.isnull().sum().sum()
    print(f"  Initial null count: {initial_nulls}")

    # Drop rows missing critical identifiers
    critical_cols = ["EmployeeID", "Attrition"]
    before = len(df)
    df = df.dropna(subset=[c for c in critical_cols if c in df.columns])
    dropped = before - len(df)
    if dropped > 0:
        print(f"  Dropped {dropped} rows missing critical data")

    # Numeric columns - fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  Filled {col} with median: {median_val}")

    # Categorical columns - fill with mode
    # Skip ExitDate: empty strings are expected for active employees
    skip_cols = ["ExitDate"]
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if col in skip_cols:
            continue
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"
            df[col] = df[col].fillna(mode_val)
            print(f"  Filled {col} with mode: {mode_val}")

    final_nulls = df.isnull().sum().sum()
    print(f"  Final null count: {final_nulls}")
    print(f"  Handled {initial_nulls - final_nulls} missing values")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate employee records."""
    print("\nRemoving duplicates...")
    before = len(df)

    # Check for exact duplicates
    exact_dupes = df.duplicated().sum()
    if exact_dupes > 0:
        df = df.drop_duplicates()
        print(f"  Removed {exact_dupes} exact duplicate rows")

    # Check for duplicate EmployeeIDs
    if "EmployeeID" in df.columns:
        id_dupes = df["EmployeeID"].duplicated().sum()
        if id_dupes > 0:
            df = df.drop_duplicates(subset=["EmployeeID"], keep="first")
            print(f"  Removed {id_dupes} duplicate EmployeeIDs")

    after = len(df)
    print(f"  Rows before: {before}, after: {after}")
    return df


def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Correct data types for all columns."""
    print("\nCorrecting data types...")

    # Integer columns
    int_cols = [
        "Age", "Education", "JobLevel", "YearsAtCompany",
        "YearsInCurrentRole", "YearsSinceLastPromotion",
        "YearsWithCurrentManager", "DistanceFromHome",
        "EnvironmentSatisfaction", "JobSatisfaction",
        "RelationshipSatisfaction", "WorkLifeBalance",
        "PerformanceRating", "TrainingTimesLastYear",
        "StockOptionLevel"
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")

    # Employee ID
    if "EmployeeID" in df.columns:
        df["EmployeeID"] = df["EmployeeID"].astype("int64")

    # Monthly Income and Percent Salary Hike as float
    if "MonthlyIncome" in df.columns:
        df["MonthlyIncome"] = pd.to_numeric(df["MonthlyIncome"], errors="coerce")

    if "PercentSalaryHike" in df.columns:
        df["PercentSalaryHike"] = pd.to_numeric(df["PercentSalaryHike"], errors="coerce")

    # Date columns
    if "HireDate" in df.columns:
        df["HireDate"] = pd.to_datetime(df["HireDate"], errors="coerce")

    if "ExitDate" in df.columns:
        df["ExitDate"] = pd.to_datetime(df["ExitDate"], errors="coerce")

    # Categorical columns
    category_cols = [
        "Gender", "Department", "JobRole", "EducationField",
        "MaritalStatus", "BusinessTravel", "OverTime",
        "Attrition", "City", "State", "Country"
    ]
    for col in category_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    print("  Data types corrected successfully")
    return df


def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and handle outliers using IQR method."""
    print("\nHandling outliers...")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_report = []

    for col in numeric_cols:
        if col in ["EmployeeID"]:
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)

        if outlier_count > 0:
            outlier_pct = outlier_count / len(df) * 100
            outlier_report.append({
                "column": col,
                "outliers": outlier_count,
                "percentage": round(outlier_pct, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2)
            })

            # Cap extreme outliers at bounds (winsorization)
            df[col] = df[col].clip(lower_bound, upper_bound)

    if outlier_report:
        print(f"  Processed {len(outlier_report)} columns with outliers:")
        for r in outlier_report[:10]:
            print(f"    {r['column']}: {r['outliers']} outliers ({r['percentage']}%)")
    else:
        print("  No significant outliers found")

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Create new features for analysis."""
    print("\nFeature engineering...")

    # Age groups
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 24, 34, 44, 54, 100],
        labels=["Under 25", "25-34", "35-44", "45-54", "55+"],
        right=True
    )

    # Salary ranges
    df["SalaryRange"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 4999, 7500, 10000, 15000, 100000],
        labels=["Under $5K", "$5K-$7.5K", "$7.5K-$10K", "$10K-$15K", "Above $15K"],
        right=True
    )

    # Tenure groups
    df["TenureGroup"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 1, 5, 10, 100],
        labels=["0-1 Years", "2-5 Years", "6-10 Years", "10+ Years"],
        right=True
    )

    # Experience score
    df["ExperienceScore"] = (
        df["YearsAtCompany"] * 0.4 +
        df["YearsInCurrentRole"] * 0.3 +
        df["YearsWithCurrentManager"] * 0.3
    ).round(1)

    # Satisfaction composite
    satisfaction_cols = [
        "EnvironmentSatisfaction", "JobSatisfaction",
        "RelationshipSatisfaction", "WorkLifeBalance"
    ]
    df["SatisfactionScore"] = df[satisfaction_cols].mean(axis=1).round(2)

    # Attrition flag numeric
    df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

    # Is remote worker (distance > 20)
    df["IsRemoteWorker"] = (df["DistanceFromHome"] > 20).astype(int)

    # Performance composite
    df["PerformanceScore"] = (
        df["PerformanceRating"] * 0.5 +
        df["TrainingTimesLastYear"] / 6 * 0.3 +
        df["PercentSalaryHike"] / 25 * 0.2
    ).round(2)

    print(f"  Added features: AgeGroup, SalaryRange, TenureGroup, "
          f"ExperienceScore, SatisfactionScore, PerformanceScore")
    return df


def clean_data(input_path: Optional[str] = None,
               output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Main data cleaning pipeline.

    Args:
        input_path: Path to raw CSV (None = default raw data)
        output_path: Path to save cleaned data (None = default cleaned dir)

    Returns:
        Cleaned DataFrame
    """
    print_section("Data Cleaning Pipeline")

    # Load
    print("\nStep 1: Loading raw data...")
    df = load_raw_data(input_path)
    print(f"  Initial shape: {df.shape}")
    
    # Create a fresh copy
    df = df.copy()

    # Step 2: Missing values
    print(f"\nStep 2: Handling missing values...")
    df = handle_missing_values(df)

    # Step 3: Duplicates
    print(f"\nStep 3: Removing duplicates...")
    df = remove_duplicates(df)

    # Step 4: Outliers (before type conversion to avoid Int64 clipping issues)
    print(f"\nStep 4: Handling outliers...")
    df = handle_outliers(df)

    # Step 5: Data types
    print(f"\nStep 5: Correcting data types...")
    df = correct_data_types(df)

    # Step 6: Feature engineering
    print(f"\nStep 6: Feature engineering...")
    df = feature_engineering(df)

    # Step 7: Standardize columns to snake_case
    print(f"\nStep 7: Standardizing column names...")
    df = standardize_columns(df)

    # Save
    if output_path is None:
        output_path = os.path.join(DATA_CLEANED_DIR, "hr_data_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"\n[SAVED] Cleaned data to: {output_path}")

    # Stats
    print(f"\n{'=' * 60}")
    print(f"  Cleaning Summary:")
    print(f"  Final shape: {df.shape}")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"{'=' * 60}")

    return df


if __name__ == "__main__":
    df = clean_data()
    print(f"\nCleaned dataset preview:")
    print(df.head())
