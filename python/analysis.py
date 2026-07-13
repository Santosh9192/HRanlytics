#!/usr/bin/env python3
"""
HR Data Analysis Module
=======================
Performs comprehensive business analysis on HR data including:
- Departmental analysis
- Attrition deep-dive
- Salary & compensation analysis
- Promotion trends
- Diversity metrics
- Satisfaction & performance analysis
- Correlation analysis
"""

import pandas as pd
import numpy as np
import os
import sys
from typing import Dict, Any, Optional, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics_utils import (
    load_raw_data, load_cleaned_data, save_processed_data,
    calculate_kpis, print_section, DATA_PROCESSED_DIR,
    SATISFACTION_LABELS, PERFORMANCE_LABELS, EDUCATION_LABELS,
    get_age_group, get_salary_range, get_tenure_group, get_risk_category
)


class HRDataAnalyzer:
    """Performs comprehensive HR analytics."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.kpis = calculate_kpis(df)
        self.insights: List[str] = []

    def add_insight(self, insight: str):
        """Add a business insight."""
        self.insights.append(insight)

    def analyze_departments(self) -> pd.DataFrame:
        """Analyze employee distribution by department."""
        print_section("Department Analysis")

        dept_analysis = self.df.groupby("department", observed=True).agg(
            employee_count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean"),
            avg_age=("age", "mean"),
            avg_tenure=("years_at_company", "mean"),
            avg_performance=("performance_rating", "mean"),
            avg_satisfaction=("job_satisfaction", "mean"),
            attrition_count=("attrition", lambda x: (x == "Yes").sum()),
            overtime_count=("overtime", lambda x: (x == "Yes").sum()),
            female_count=("gender", lambda x: (x == "Female").sum())
        ).round(2)

        dept_analysis["attrition_rate"] = (
            dept_analysis["attrition_count"] / dept_analysis["employee_count"] * 100
        ).round(2)
        dept_analysis["overtime_pct"] = (
            dept_analysis["overtime_count"] / dept_analysis["employee_count"] * 100
        ).round(2)
        dept_analysis["female_pct"] = (
            dept_analysis["female_count"] / dept_analysis["employee_count"] * 100
        ).round(2)
        dept_analysis["total_salary_cost"] = (
            self.df.groupby("department", observed=True)["monthly_income"].sum()
        ).round(2)

        dept_analysis = dept_analysis.sort_values("employee_count", ascending=False)

        print(dept_analysis.to_string())
        save_processed_data(dept_analysis.reset_index(), "department_analysis.csv")

        # Generate insights
        top_attrition = dept_analysis["attrition_rate"].idxmax()
        top_overtime = dept_analysis["overtime_pct"].idxmax()
        self.add_insight(
            f"{top_attrition} has the highest attrition rate at "
            f"{dept_analysis.loc[top_attrition, 'attrition_rate']:.1f}%"
        )
        self.add_insight(
            f"{top_overtime} has the highest overtime percentage at "
            f"{dept_analysis.loc[top_overtime, 'overtime_pct']:.1f}%"
        )

        return dept_analysis

    def analyze_attrition(self) -> pd.DataFrame:
        """Deep-dive attrition analysis."""
        print_section("Attrition Analysis")

        total = len(self.df)
        attrited = self.df[self.df["attrition"] == "Yes"]
        active = self.df[self.df["attrition"] == "No"]

        print(f"Attrition Rate: {self.kpis['attrition_rate']:.1f}%")
        print(f"Total Attrited: {len(attrited)}")
        print(f"Total Active: {len(active)}")

        # Attrition by department
        dept_attr = self.df.groupby("department", observed=True).agg(
            total=("employee_id", "count"),
            attrited=("attrition", lambda x: (x == "Yes").sum())
        )
        dept_attr["attrition_rate"] = (dept_attr["attrited"] / dept_attr["total"] * 100).round(2)
        dept_attr = dept_attr.sort_values("attrition_rate", ascending=False)

        print("\nAttrition Rate by Department:")
        print(dept_attr.to_string())

        # Attrition by key factors
        factors = ["gender", "job_level", "marital_status", "overtime", "business_travel"]
        for factor in factors:
            print(f"\nAttrition by {factor.replace('_', ' ').title()}:")
            factor_attr = self.df.groupby(factor, observed=True).agg(
                total=("employee_id", "count"),
                attrited=("attrition", lambda x: (x == "Yes").sum())
            )
            factor_attr["attrition_rate"] = (
                factor_attr["attrited"] / factor_attr["total"] * 100
            ).round(2)
            print(factor_attr.to_string())

        # Compare attrited vs active
        comparison = pd.DataFrame({
            "metric": ["avg_age", "avg_monthly_income", "avg_tenure",
                       "avg_job_satisfaction", "avg_work_life_balance",
                       "avg_performance", "avg_years_since_promotion"],
            "attrited": [
                attrited["age"].mean(),
                attrited["monthly_income"].mean(),
                attrited["years_at_company"].mean(),
                attrited["job_satisfaction"].mean(),
                attrited["work_life_balance"].mean(),
                attrited["performance_rating"].mean(),
                attrited["years_since_last_promotion"].mean()
            ],
            "active": [
                active["age"].mean(),
                active["monthly_income"].mean(),
                active["years_at_company"].mean(),
                active["job_satisfaction"].mean(),
                active["work_life_balance"].mean(),
                active["performance_rating"].mean(),
                active["years_since_last_promotion"].mean()
            ]
        }).round(2)
        comparison["difference"] = comparison["attrited"] - comparison["active"]

        print("\nAttrited vs Active Comparison:")
        print(comparison.to_string())

        save_processed_data(dept_attr.reset_index(), "attrition_by_department.csv")
        save_processed_data(comparison, "attrition_comparison.csv")

        # Insights
        top_attr_dept = dept_attr.index[0]
        self.add_insight(
            f"Employees who left had {comparison.loc[
                comparison['metric'] == 'avg_job_satisfaction', 'difference'
            ].values[0]:.2f} lower job satisfaction on average"
        )

        return dept_attr

    def analyze_salary(self) -> pd.DataFrame:
        """Salary and compensation analysis."""
        print_section("Salary Analysis")

        # Salary stats by department
        dept_salary = self.df.groupby("department", observed=True).agg(
            employee_count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean"),
            median_salary=("monthly_income", "median"),
            min_salary=("monthly_income", "min"),
            max_salary=("monthly_income", "max"),
            std_salary=("monthly_income", "std"),
            avg_hike=("percent_salary_hike", "mean")
        ).round(2).sort_values("avg_salary", ascending=False)

        print("\nSalary by Department:")
        print(dept_salary.to_string())

        # Gender pay gap analysis
        gender_pay = self.df.groupby(["department", "gender"], observed=True).agg(
            avg_salary=("monthly_income", "mean"),
            count=("employee_id", "count")
        ).round(2)

        print("\nGender Pay Analysis:")
        print(gender_pay.to_string())

        # Salary by education
        edu_salary = self.df.groupby("education", observed=True).agg(
            count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean"),
            avg_hike=("percent_salary_hike", "mean")
        ).round(2)
        edu_salary.index = edu_salary.index.map(EDUCATION_LABELS)

        print("\nSalary by Education Level:")
        print(edu_salary.to_string())

        save_processed_data(dept_salary.reset_index(), "salary_by_department.csv")
        save_processed_data(gender_pay.reset_index(), "gender_pay_analysis.csv")
        save_processed_data(edu_salary.reset_index(), "salary_by_education.csv")

        # Insights
        top_paying = dept_salary.index[0]
        self.add_insight(
            f"{top_paying} pays the highest average salary at "
            f"${dept_salary.loc[top_paying, 'avg_salary']:,.0f}/month"
        )

        return dept_salary

    def analyze_promotion(self) -> pd.DataFrame:
        """Promotion and career progression analysis."""
        print_section("Promotion Analysis")

        # Promotion rate by department
        dept_promo = self.df.groupby("department", observed=True).agg(
            total=("employee_id", "count"),
            avg_years_since_promotion=("years_since_last_promotion", "mean"),
            promoted_recent=("years_since_last_promotion",
                            lambda x: (x == 0).sum()),
            overdue_promotion=("years_since_last_promotion",
                              lambda x: (x >= 3).sum())
        ).round(2)
        dept_promo["promotion_rate"] = (
            dept_promo["promoted_recent"] / dept_promo["total"] * 100
        ).round(2)
        dept_promo["overdue_pct"] = (
            dept_promo["overdue_promotion"] / dept_promo["total"] * 100
        ).round(2)
        dept_promo = dept_promo.sort_values("promotion_rate", ascending=False)

        print("\nPromotion Analysis by Department:")
        print(dept_promo.to_string())

        # Promotion by performance
        perf_promo = self.df.groupby("performance_rating", observed=True).agg(
            total=("employee_id", "count"),
            promoted=("years_since_last_promotion", lambda x: (x == 0).sum()),
            avg_years=("years_since_last_promotion", "mean")
        ).round(2)
        perf_promo["promotion_rate"] = (
            perf_promo["promoted"] / perf_promo["total"] * 100
        ).round(2)

        print("\nPromotion Rate by Performance:")
        print(perf_promo.to_string())

        save_processed_data(dept_promo.reset_index(), "promotion_analysis.csv")

        # Insight
        most_overdue = dept_promo["overdue_pct"].idxmax()
        self.add_insight(
            f"{most_overdue} has the highest percentage ({dept_promo.loc[most_overdue, 'overdue_pct']:.1f}%) "
            f"of employees overdue for promotion (3+ years)"
        )

        return dept_promo

    def analyze_diversity(self) -> pd.DataFrame:
        """Diversity and inclusion analysis."""
        print_section("Diversity Analysis")

        # Gender diversity by department
        dept_div = self.df.groupby("department", observed=True).agg(
            total=("employee_id", "count"),
            male=("gender", lambda x: (x == "Male").sum()),
            female=("gender", lambda x: (x == "Female").sum())
        ).round(2)
        dept_div["female_pct"] = (
            dept_div["female"] / dept_div["total"] * 100
        ).round(2)
        dept_div["male_pct"] = (
            dept_div["male"] / dept_div["total"] * 100
        ).round(2)
        dept_div = dept_div.sort_values("female_pct", ascending=False)

        print("\nGender Diversity by Department:")
        print(dept_div.to_string())

        # Age diversity
        self.df["age_group"] = self.df["age"].apply(get_age_group)
        age_div = self.df.groupby("age_group", observed=True).agg(
            count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean")
        ).round(2)

        print("\nAge Distribution:")
        print(age_div.to_string())

        # Education diversity
        edu_div = self.df.groupby("education_field", observed=True).agg(
            count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean")
        ).round(2).sort_values("count", ascending=False)

        print("\nEducation Field Distribution:")
        print(edu_div.to_string())

        save_processed_data(dept_div.reset_index(), "diversity_by_department.csv")
        save_processed_data(age_div.reset_index(), "age_distribution.csv")

        return dept_div

    def analyze_satisfaction(self) -> pd.DataFrame:
        """Employee satisfaction and work-life balance analysis."""
        print_section("Satisfaction Analysis")

        sat_cols = ["job_satisfaction", "environment_satisfaction",
                    "relationship_satisfaction", "work_life_balance"]

        # Average satisfaction by department
        dept_sat = self.df.groupby("department", observed=True)[sat_cols].mean().round(2)
        dept_sat.columns = [c.replace("_", " ").title() for c in sat_cols]
        dept_sat = dept_sat.sort_values("Job Satisfaction", ascending=False)

        print("\nSatisfaction Scores by Department:")
        print(dept_sat.to_string())

        # Satisfaction distribution
        for col in sat_cols:
            dist = self.df[col].value_counts().sort_index()
            dist.index = dist.index.map(SATISFACTION_LABELS)
            print(f"\n{col.replace('_', ' ').title()} Distribution:")
            print(dist.to_string())

        save_processed_data(dept_sat.reset_index(), "satisfaction_analysis.csv")

        return dept_sat

    def analyze_performance(self) -> pd.DataFrame:
        """Performance analysis."""
        print_section("Performance Analysis")

        # Performance by department
        dept_perf = self.df.groupby("department", observed=True).agg(
            avg_performance=("performance_rating", "mean"),
            excellent=("performance_rating", lambda x: (x == 4).sum()),
            good=("performance_rating", lambda x: (x == 3).sum()),
            avg_training=("training_times_last_year", "mean"),
            avg_hike=("percent_salary_hike", "mean")
        ).round(2).sort_values("avg_performance", ascending=False)

        print("\nPerformance by Department:")
        print(dept_perf.to_string())

        # Performance vs training
        perf_vs_training = self.df.groupby("performance_rating", observed=True).agg(
            count=("employee_id", "count"),
            avg_training=("training_times_last_year", "mean"),
            avg_salary_hike=("percent_salary_hike", "mean")
        ).round(2)

        print("\nPerformance vs Training:")
        print(perf_vs_training.to_string())

        save_processed_data(dept_perf.reset_index(), "performance_analysis.csv")

        return dept_perf

    def analyze_correlations(self) -> pd.DataFrame:
        """Correlation analysis between key metrics."""
        print_section("Correlation Analysis")

        numeric_cols = [
            "age", "monthly_income", "years_at_company",
            "job_satisfaction", "work_life_balance",
            "performance_rating", "training_times_last_year",
            "percent_salary_hike", "years_since_last_promotion",
            "environment_satisfaction"
        ]

        corr_matrix = self.df[numeric_cols].corr().round(3)

        print("\nCorrelation Matrix (Key Metrics):")
        print(corr_matrix.to_string())

        # Find strongest correlations
        correlation_pairs = []
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                corr = corr_matrix.loc[col1, col2]
                correlation_pairs.append({
                    "variable_1": col1.replace("_", " ").title(),
                    "variable_2": col2.replace("_", " ").title(),
                    "correlation": corr,
                    "strength": abs(corr)
                })

        corr_df = pd.DataFrame(correlation_pairs)
        corr_df = corr_df.sort_values("strength", ascending=False)

        print("\nTop 10 Strongest Correlations:")
        print(corr_df.head(10).to_string())

        save_processed_data(corr_df, "correlation_analysis.csv")

        return corr_df

    def analyze_training(self) -> pd.DataFrame:
        """Training and development analysis."""
        print_section("Training Analysis")

        train_dept = self.df.groupby("department", observed=True).agg(
            total_employees=("employee_id", "count"),
            total_training=("training_times_last_year", "sum"),
            avg_training=("training_times_last_year", "mean"),
            min_training=("training_times_last_year", "min"),
            max_training=("training_times_last_year", "max"),
            avg_performance=("performance_rating", "mean")
        ).round(2).sort_values("avg_training", ascending=False)

        print("\nTraining Analysis by Department:")
        print(train_dept.to_string())

        save_processed_data(train_dept.reset_index(), "training_analysis.csv")

        return train_dept

    def risk_assessment(self) -> pd.DataFrame:
        """Employee flight risk assessment."""
        print_section("Risk Assessment")

        risk_data = self.df[self.df["attrition"] == "No"].copy()
        risk_data["risk_category"] = risk_data.apply(get_risk_category, axis=1)

        risk_summary = risk_data.groupby("risk_category", observed=True).agg(
            count=("employee_id", "count"),
            avg_salary=("monthly_income", "mean"),
            avg_satisfaction=("job_satisfaction", "mean"),
            avg_tenure=("years_at_company", "mean")
        ).round(2)

        print("\nEmployee Risk Distribution (Active Employees):")
        print(risk_summary.to_string())

        # High risk by department
        high_risk = risk_data[risk_data["risk_category"] == "High Risk"]
        dept_risk = high_risk.groupby("department", observed=True).agg(
            high_risk_count=("employee_id", "count")
        ).sort_values("high_risk_count", ascending=False)

        print("\nHigh Risk Employees by Department:")
        print(dept_risk.to_string())

        save_processed_data(risk_summary.reset_index(), "risk_assessment.csv")
        save_processed_data(dept_risk.reset_index(), "high_risk_by_dept.csv")

        return risk_summary

    def run_all_analyses(self) -> Dict[str, Any]:
        """Run all analysis functions."""
        print_section("COMPREHENSIVE HR ANALYSIS")
        print(f"Dataset: {len(self.df):,} employees")
        print(f"Total KPIs calculated: {len(self.kpis)}")

        results = {
            "kpis": self.kpis,
            "departments": self.analyze_departments(),
            "attrition": self.analyze_attrition(),
            "salary": self.analyze_salary(),
            "promotion": self.analyze_promotion(),
            "diversity": self.analyze_diversity(),
            "satisfaction": self.analyze_satisfaction(),
            "performance": self.analyze_performance(),
            "correlations": self.analyze_correlations(),
            "training": self.analyze_training(),
            "risk_assessment": self.risk_assessment()
        }

        # Summary insights
        print_section("KEY BUSINESS INSIGHTS")
        for i, insight in enumerate(self.insights, 1):
            print(f"  {i}. {insight}")

        # Save insights
        insights_df = pd.DataFrame({"insights": self.insights})
        save_processed_data(insights_df, "business_insights.csv")

        # Save KPIs
        kpis_df = pd.DataFrame([self.kpis])
        save_processed_data(kpis_df, "kpi_summary.csv")

        return results


def run_analysis(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Main analysis entry point."""
    from analytics_utils import standardize_columns
    # Try cleaned data first
    if file_path is None:
        cleaned_path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "data", "cleaned", "hr_data_cleaned.csv")
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
            print(f"Loaded cleaned data: {cleaned_path}")
        else:
            df = load_raw_data()
            df = standardize_columns(df)
    else:
        df = pd.read_csv(file_path)
        df = standardize_columns(df)

    analyzer = HRDataAnalyzer(df)
    return analyzer.run_all_analyses()


if __name__ == "__main__":
    results = run_analysis()
    print("\nAnalysis complete! All reports saved.")
