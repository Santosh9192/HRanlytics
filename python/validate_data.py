#!/usr/bin/env python3
"""
Data Validation Module
======================
Validates data quality, integrity, and business rules.
Generates validation reports with pass/fail status for each check.
"""

import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics_utils import (
    load_raw_data, print_section, DATA_CLEANED_DIR,
    COLUMN_MAPPING
)


class DataValidator:
    """Validates HR dataset against quality rules and business constraints."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.results: List[Dict[str, Any]] = []
        self.total_checks = 0
        self.passed_checks = 0
        self.failed_checks = 0

    def _add_result(self, check_name: str, passed: bool,
                    details: str, severity: str = "medium"):
        """Add a validation result."""
        self.total_checks += 1
        if passed:
            self.passed_checks += 1
        else:
            self.failed_checks += 1

        self.results.append({
            "check_name": check_name,
            "passed": passed,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "PASS" if passed else "FAIL"
        })

    # ─── Missing Data Checks ───

    def check_missing_values(self):
        """Check for missing values in critical columns."""
        critical_cols = [
            "employee_id", "employee_name", "age", "gender",
            "department", "monthly_income", "attrition", "hire_date"
        ]

        for col in critical_cols:
            if col in self.df.columns:
                null_count = self.df[col].isnull().sum()
                null_pct = null_count / len(self.df) * 100
                passed = null_pct < 5  # Less than 5% missing
                self._add_result(
                    f"Missing values in {col}",
                    passed,
                    f"{null_count} missing ({null_pct:.2f}%)",
                    "high" if col in ["employee_id", "attrition"] else "medium"
                )

    def check_overall_missing(self):
        """Overall missing data percentage."""
        total_cells = self.df.shape[0] * self.df.shape[1]
        total_missing = self.df.isnull().sum().sum()
        missing_pct = total_missing / total_cells * 100
        passed = missing_pct < 10
        self._add_result(
            "Overall missing data",
            passed,
            f"{total_missing} missing cells out of {total_cells} ({missing_pct:.2f}%)"
        )

    # ─── Data Type Checks ───

    def check_numeric_columns(self):
        """Verify numeric columns have valid numeric types."""
        expected_numeric = ["age", "monthly_income", "job_level", "years_at_company",
                            "years_in_current_role", "years_since_last_promotion",
                            "performance_rating", "job_satisfaction"]

        for col in expected_numeric:
            if col in self.df.columns:
                non_numeric = pd.to_numeric(self.df[col], errors="coerce").isnull().sum()
                passed = non_numeric == 0
                self._add_result(
                    f"Numeric type check: {col}",
                    passed,
                    f"{non_numeric} non-numeric values found"
                )

    def check_date_columns(self):
        """Verify date columns have valid dates."""
        date_cols = ["hire_date", "exit_date"]
        for col in date_cols:
            if col not in self.df.columns:
                continue
            if col == "exit_date" and "attrition" in self.df.columns:
                # Only validate exit dates for attrited employees
                attrited = self.df[self.df["attrition"] == "Yes"]
                if len(attrited) > 0:
                    invalid_dates = pd.to_datetime(attrited[col], errors="coerce").isnull().sum()
                    passed = invalid_dates == 0
                    self._add_result(
                        f"Date validity check: {col}",
                        passed,
                        f"{invalid_dates} invalid exit dates found (attrited employees)"
                    )
                else:
                    self._add_result(f"Date validity check: {col}", True,
                                     "No attrited employees to validate")
            else:
                invalid_dates = pd.to_datetime(self.df[col], errors="coerce").isnull().sum()
                passed = invalid_dates == 0
                self._add_result(
                    f"Date validity check: {col}",
                    passed,
                    f"{invalid_dates} invalid dates found"
                )

    # ─── Range Checks ───

    def check_age_range(self):
        """Verify age is within valid range."""
        if "age" in self.df.columns:
            invalid = ((self.df["age"] < 18) | (self.df["age"] > 80)).sum()
            passed = invalid == 0
            self._add_result(
                "Age range check (18-80)",
                passed,
                f"{invalid} records with invalid age",
                severity="high"
            )

    def check_salary_range(self):
        """Verify salary is within valid range."""
        if "monthly_income" in self.df.columns:
            invalid = (self.df["monthly_income"] <= 0).sum()
            passed = invalid == 0
            self._add_result(
                "Salary > $0 check",
                passed,
                f"{invalid} records with zero/negative salary",
                severity="high"
            )

    def check_satisfaction_range(self):
        """Verify satisfaction scores are 1-4."""
        sat_cols = [
            "job_satisfaction", "environment_satisfaction",
            "relationship_satisfaction", "work_life_balance"
        ]
        for col in sat_cols:
            if col in self.df.columns:
                invalid = ((self.df[col] < 1) | (self.df[col] > 4)).sum()
                passed = invalid == 0
                self._add_result(
                    f"{col} range check (1-4)",
                    passed,
                    f"{invalid} out of range"
                )

    def check_performance_range(self):
        """Verify performance rating is 1-4."""
        if "performance_rating" in self.df.columns:
            invalid = ((self.df["performance_rating"] < 1) |
                       (self.df["performance_rating"] > 4)).sum()
            passed = invalid == 0
            self._add_result(
                "Performance rating range (1-4)",
                passed,
                f"{invalid} out of range"
            )

    def check_experience_years_range(self):
        """Verify years of experience are non-negative and reasonable."""
        yr_cols = ["years_at_company", "years_in_current_role",
                   "years_since_last_promotion", "years_with_current_manager"]
        for col in yr_cols:
            if col in self.df.columns:
                negative = (self.df[col] < 0).sum()
                passed = negative == 0
                self._add_result(
                    f"{col} non-negative check",
                    passed,
                    f"{negative} negative values"
                )

    # ─── Uniqueness Checks ───

    def check_employee_id_uniqueness(self):
        """Verify EmployeeID is unique."""
        if "employee_id" in self.df.columns:
            dupes = self.df["employee_id"].duplicated().sum()
            passed = dupes == 0
            self._add_result(
                "EmployeeID uniqueness",
                passed,
                f"{dupes} duplicate IDs found",
                severity="high"
            )

    # ─── Business Rule Checks ───

    def check_attrition_logic(self):
        """Verify attrition logic: 'Yes' should have exit dates, 'No' should not."""
        if "attrition" in self.df.columns and "exit_date" in self.df.columns:
            # Attrited employees should have exit dates
            attrited_no_exit = (
                (self.df["attrition"] == "Yes") &
                (self.df["exit_date"].isnull())
            ).sum()

            no_attrition_with_exit = (
                (self.df["attrition"] == "No") &
                (self.df["exit_date"].notna())
            ).sum()

            passed = (attrited_no_exit == 0) and (no_attrition_with_exit == 0)
            self._add_result(
                "Attrition-ExitDate consistency",
                passed,
                f"{attrited_no_exit} attrited without exit date, "
                f"{no_attrition_with_exit} active with exit date",
                severity="high"
            )

    def check_hire_before_exit(self):
        """Verify exit date is after hire date."""
        if "hire_date" in self.df.columns and "exit_date" in self.df.columns:
            valid_dates = self.df["hire_date"].notna() & self.df["exit_date"].notna()
            if valid_dates.any():
                hire_before_exit = (self.df.loc[valid_dates, "exit_date"] >=
                                    self.df.loc[valid_dates, "hire_date"]).all()
                passed = hire_before_exit
                self._add_result(
                    "Hire date before exit date",
                    passed,
                    "Some exit dates are before hire dates" if not passed else "All valid",
                    severity="critical"
                )

    def check_gender_values(self):
        """Verify gender has valid values."""
        if "gender" in self.df.columns:
            valid_values = self.df["gender"].isin(["Male", "Female"])
            invalid = (~valid_values).sum()
            passed = invalid == 0
            self._add_result(
                "Gender valid values",
                passed,
                f"{invalid} invalid gender values"
            )

    def check_attrition_values(self):
        """Verify attrition has valid values."""
        if "attrition" in self.df.columns:
            valid_values = self.df["attrition"].isin(["Yes", "No"])
            invalid = (~valid_values).sum()
            passed = invalid == 0
            self._add_result(
                "Attrition valid values",
                passed,
                f"{invalid} invalid attrition values"
            )

    # ─── Statistical Checks ───

    def check_outlier_percentage(self):
        """Check percentage of outliers in key numeric columns."""
        numeric_cols = ["age", "monthly_income", "years_at_company"]
        for col in numeric_cols:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((self.df[col] < Q1 - 1.5 * IQR) |
                           (self.df[col] > Q3 + 1.5 * IQR)).sum()
                outlier_pct = outliers / len(self.df) * 100
                passed = outlier_pct < 15  # Less than 15% outliers
                self._add_result(
                    f"Outlier check: {col}",
                    passed,
                    f"{outliers} outliers ({outlier_pct:.2f}%)"
                )

    def check_zero_values(self):
        """Check for unexpected zero values."""
        expected_positive = ["years_at_company", "monthly_income"]
        for col in expected_positive:
            if col in self.df.columns:
                zeros = (self.df[col] == 0).sum()
                passed = zeros < len(self.df) * 0.05  # Less than 5%
                self._add_result(
                    f"Zero value check: {col}",
                    passed,
                    f"{zeros} zero values found"
                )

    # ─── Run All Checks ───

    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks."""
        print_section("Data Validation")

        print("\nRunning validation checks...")

        # Missing data
        self.check_missing_values()
        self.check_overall_missing()

        # Data types
        self.check_numeric_columns()
        self.check_date_columns()

        # Range checks
        self.check_age_range()
        self.check_salary_range()
        self.check_satisfaction_range()
        self.check_performance_range()
        self.check_experience_years_range()

        # Uniqueness
        self.check_employee_id_uniqueness()

        # Business rules
        self.check_attrition_logic()
        self.check_hire_before_exit()
        self.check_gender_values()
        self.check_attrition_values()

        # Statistical
        self.check_outlier_percentage()
        self.check_zero_values()

        # Summary
        print(f"\n  Validation Complete:")
        print(f"  Total checks: {self.total_checks}")
        print(f"  Passed: {self.passed_checks}")
        print(f"  Failed: {self.failed_checks}")
        print(f"  Pass rate: {self.passed_checks / self.total_checks * 100:.1f}%")

        # Print failures
        failures = [r for r in self.results if not r["passed"]]
        if failures:
            print(f"\n  Failed Checks:")
            for f in failures:
                print(f"    [FAIL] {f['check_name']}: {f['details']}")

        return {
            "total_checks": self.total_checks,
            "passed": self.passed_checks,
            "failed": self.failed_checks,
            "pass_rate": round(self.passed_checks / self.total_checks * 100, 1),
            "results": self.results,
            "failures": failures,
            "validation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def validate_data(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Main validation entry point."""
    if file_path is None:
        # First try cleaned, then raw
        cleaned_path = os.path.join(DATA_CLEANED_DIR, "hr_data_cleaned.csv")
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
            print(f"Validating cleaned data: {cleaned_path}")
        else:
            df = load_raw_data()
            print("Validating raw data")
    else:
        df = pd.read_csv(file_path)
        print(f"Validating data: {file_path}")

    # Standardize column names so validation checks work consistently
    df = df.rename(columns=COLUMN_MAPPING)

    print(f"Dataset: {df.shape[0]} rows x {df.shape[1]} columns")

    validator = DataValidator(df)
    return validator.validate_all()


if __name__ == "__main__":
    results = validate_data()

    # Save validation report
    report_path = os.path.join(DATA_CLEANED_DIR, "validation_report.json")
    with open(report_path, "w") as f:
        # Convert non-serializable items
        report = {
            "summary": {
                "total_checks": results["total_checks"],
                "passed": results["passed"],
                "failed": results["failed"],
                "pass_rate": results["pass_rate"],
                "validation_date": results["validation_date"]
            },
            "results": [
                {
                    "check_name": r["check_name"],
                    "status": r["status"],
                    "details": r["details"],
                    "severity": r["severity"]
                }
                for r in results["results"]
            ]
        }
        json.dump(report, f, indent=2)
    print(f"\n[SAVED] Validation report: {report_path}")
