#!/usr/bin/env python3
"""
Chart Generation Module
=======================
Generates professional visualizations using Matplotlib and Plotly.
Creates static (PNG) and interactive (HTML) charts for HR analytics.
"""

import pandas as pd
import numpy as np
import os
import sys
import warnings
from typing import Optional, List, Dict, Any

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Plotly for interactive charts
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics_utils import (
    load_raw_data, standardize_columns,
    print_section, DATA_PROCESSED_DIR, REPORTS_HTML_DIR, PROJECT_ROOT,
    SATISFACTION_LABELS, PERFORMANCE_LABELS, EDUCATION_LABELS
)

# Output directories
CHARTS_STATIC_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")
os.makedirs(CHARTS_STATIC_DIR, exist_ok=True)
os.makedirs(REPORTS_HTML_DIR, exist_ok=True)

# Color palette
COLORS = {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#06B6D4",
    "dark": "#1E293B",
    "light": "#F8FAFC",
    "gray": "#94A3B8"
}

PALETTE = ["#2563EB", "#7C3AED", "#10B981", "#EF4444",
           "#F59E0B", "#06B6D4", "#8B5CF6", "#EC4899"]

# Matplotlib style settings
plt.style.use("default")
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.fontsize": 10,
    "figure.facecolor": "white",
    "axes.facecolor": "white"
})


def setup_plot(title: str, xlabel: str = "", ylabel: str = ""):
    """Setup a matplotlib plot with consistent styling."""
    fig, ax = plt.subplots()
    ax.set_title(title, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(colors=COLORS["dark"])
    return fig, ax


def save_static_chart(fig, filename: str):
    """Save matplotlib figure as PNG."""
    filepath = os.path.join(CHARTS_STATIC_DIR, filename)
    fig.savefig(filepath, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"[SAVED] Static chart: {filepath}")
    return filepath


def save_interactive_chart(fig, filename: str):
    """Save plotly figure as HTML."""
    filepath = os.path.join(REPORTS_HTML_DIR, filename)
    fig.write_html(filepath, include_plotlyjs="cdn")
    print(f"[SAVED] Interactive chart: {filepath}")
    return filepath


def plot_employee_distribution(df: pd.DataFrame):
    """Chart 1: Employee distribution by department."""
    print("Generating: Employee Distribution by Department...")
    dept_counts = df["department"].value_counts()

    fig, ax = setup_plot("Employee Distribution by Department",
                         "Department", "Number of Employees")
    bars = ax.bar(dept_counts.index, dept_counts.values, color=PALETTE[0],
                  edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, dept_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                str(val), ha="center", va="bottom", fontsize=9)

    ax.set_xticklabels(dept_counts.index, rotation=45, ha="right", fontsize=9)
    fig.tight_layout()
    save_static_chart(fig, "employee_distribution.png")


def plot_gender_diversity(df: pd.DataFrame):
    """Chart 2: Gender diversity by department."""
    print("Generating: Gender Diversity by Department...")

    dept_gender = df.groupby(["department", "gender"]).size().unstack(fill_value=0)
    dept_gender.plot(
        kind="bar", stacked=True, color=[COLORS["primary"], COLORS["secondary"]],
        edgecolor="white", linewidth=0.5, figsize=(12, 6)
    )
    plt.title("Gender Diversity by Department", fontweight="bold", pad=15)
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.legend(title="Gender")
    plt.tight_layout()
    save_static_chart(plt.gcf(), "gender_diversity.png")


def plot_attrition_rate(df: pd.DataFrame):
    """Chart 3: Attrition rate by department."""
    print("Generating: Attrition Rate by Department...")

    dept_attr = df.groupby("department")["attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=True)

    colors = [COLORS["danger"] if v > 20 else COLORS["warning"] if v > 15 else COLORS["success"]
              for v in dept_attr.values]

    fig, ax = setup_plot("Attrition Rate by Department (%)",
                         "Attrition Rate (%)", "Department")
    bars = ax.barh(dept_attr.index, dept_attr.values, color=colors, edgecolor="white")

    for bar, val in zip(bars, dept_attr.values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=9)

    fig.tight_layout()
    save_static_chart(fig, "attrition_rate.png")


def plot_salary_distribution(df: pd.DataFrame):
    """Chart 4: Salary distribution by department."""
    print("Generating: Salary Distribution by Department...")

    dept_salary = df.groupby("department")["monthly_income"].agg(["mean", "median", "std"]).round(2)
    dept_salary = dept_salary.sort_values("mean", ascending=True)

    fig, ax = setup_plot("Average Monthly Salary by Department",
                         "Average Salary ($)", "Department")
    bars = ax.barh(dept_salary.index, dept_salary["mean"], color=PALETTE[2],
                   edgecolor="white", xerr=dept_salary["std"], capsize=3)

    for bar, val in zip(bars, dept_salary["mean"]):
        ax.text(bar.get_width() + 200, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", fontsize=8)

    fig.tight_layout()
    save_static_chart(fig, "salary_distribution.png")


def plot_age_distribution(df: pd.DataFrame):
    """Chart 5: Age distribution histogram."""
    print("Generating: Age Distribution...")

    fig, ax = setup_plot("Employee Age Distribution", "Age", "Number of Employees")
    ax.hist(df["age"], bins=15, color=PALETTE[0], edgecolor="white",
            linewidth=0.5, alpha=0.8)
    ax.axvline(df["age"].mean(), color=COLORS["danger"], linestyle="--",
               linewidth=2, label=f"Mean: {df['age'].mean():.1f}")
    ax.axvline(df["age"].median(), color=COLORS["success"], linestyle=":",
               linewidth=2, label=f"Median: {df['age'].median():.1f}")
    ax.legend()
    fig.tight_layout()
    save_static_chart(fig, "age_distribution.png")


def plot_satisfaction_scores(df: pd.DataFrame):
    """Chart 6: Satisfaction scores heatmap."""
    print("Generating: Satisfaction Scores...")

    sat_cols = ["job_satisfaction", "environment_satisfaction",
                "relationship_satisfaction", "work_life_balance"]
    sat_labels = ["Job", "Environment", "Relationship", "Work-Life Balance"]
    sat_data = df[sat_cols].mean().round(2)

    fig, ax = setup_plot("Average Satisfaction Scores", "Satisfaction Type", "Score (1-4)")
    bars = ax.bar(sat_labels, sat_data.values, color=[PALETTE[i] for i in range(4)],
                  edgecolor="white", width=0.6)

    for bar, val in zip(bars, sat_data.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_ylim(0, 4.5)
    fig.tight_layout()
    save_static_chart(fig, "satisfaction_scores.png")


def plot_performance_vs_salary(df: pd.DataFrame):
    """Chart 7: Performance rating vs salary box plot."""
    print("Generating: Performance vs Salary...")

    fig, ax = setup_plot("Salary Distribution by Performance Rating",
                         "Performance Rating", "Monthly Income ($)")

    perf_groups = [df[df["performance_rating"] == r]["monthly_income"].values
                   for r in sorted(df["performance_rating"].unique())]
    labels = [PERFORMANCE_LABELS[r] for r in sorted(df["performance_rating"].unique())]

    bp = ax.boxplot(perf_groups, tick_labels=labels, patch_artist=True,
                    widths=0.6)
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    fig.tight_layout()
    save_static_chart(fig, "performance_vs_salary.png")


def plot_overtime_impact(df: pd.DataFrame):
    """Chart 8: Overtime impact on attrition."""
    print("Generating: Overtime Impact on Attrition...")

    ot_attr = df.groupby("overtime")["attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )

    fig, ax = setup_plot("Attrition Rate by Overtime Status",
                         "Overtime", "Attrition Rate (%)")
    bars = ax.bar(ot_attr.index, ot_attr.values,
                  color=[COLORS["danger"], COLORS["success"]],
                  edgecolor="white", width=0.5)

    for bar, val in zip(bars, ot_attr.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax.set_ylim(0, max(ot_attr.values) * 1.3)
    fig.tight_layout()
    save_static_chart(fig, "overtime_impact.png")


def plot_promotion_analysis(df: pd.DataFrame):
    """Chart 9: Promotion analysis."""
    print("Generating: Promotion Analysis...")

    promo_data = df["years_since_last_promotion"].value_counts().sort_index()
    promo_data = promo_data[promo_data.index <= 10]

    fig, ax = setup_plot("Years Since Last Promotion",
                         "Years", "Number of Employees")
    ax.bar(promo_data.index, promo_data.values, color=PALETTE[5],
           edgecolor="white", width=0.8)
    ax.set_xticks(promo_data.index)
    fig.tight_layout()
    save_static_chart(fig, "promotion_analysis.png")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Chart 10: Correlation heatmap."""
    print("Generating: Correlation Heatmap...")

    numeric_cols = [
        "age", "monthly_income", "years_at_company",
        "job_satisfaction", "work_life_balance",
        "performance_rating", "training_times_last_year",
        "percent_salary_hike", "years_since_last_promotion"
    ]
    labels = ["Age", "Income", "Tenure", "Job Sat.", "WLB",
              "Performance", "Training", "Salary Hike", "Promotion"]

    corr = df[numeric_cols].corr().round(2)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)

    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, f"{corr.values[i, j]:.2f}",
                          ha="center", va="center", fontsize=8,
                          color="white" if abs(corr.values[i, j]) > 0.5 else "black")

    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Correlation Heatmap", fontweight="bold", pad=15)
    fig.tight_layout()
    save_static_chart(fig, "correlation_heatmap.png")


def plot_monthly_trend(df: pd.DataFrame):
    """Chart 11: Monthly hiring trend."""
    print("Generating: Monthly Hiring Trend...")

    # Use a copy to avoid mutating the original DataFrame
    df_plot = df.copy()
    df_plot["hire_date"] = pd.to_datetime(df_plot["hire_date"])
    df_plot["year_month"] = df_plot["hire_date"].dt.to_period("M")
    monthly = df_plot.groupby("year_month").size().reset_index(name="hires")
    monthly["year_month"] = monthly["year_month"].astype(str)

    fig, ax = setup_plot("Monthly Hiring Trend", "Date", "Number of Hires")
    ax.plot(range(len(monthly)), monthly["hires"].values,
            color=PALETTE[0], linewidth=2, marker="o", markersize=4)

    # Add trend line
    z = np.polyfit(range(len(monthly)), monthly["hires"].values, 1)
    p = np.poly1d(z)
    ax.plot(range(len(monthly)), p(range(len(monthly))),
            color=COLORS["danger"], linestyle="--", alpha=0.6, label="Trend")

    ax.set_xticks(range(0, len(monthly), max(1, len(monthly) // 12)))
    ax.set_xticklabels([monthly["year_month"].iloc[i]
                       for i in range(0, len(monthly), max(1, len(monthly) // 12))],
                       rotation=45, ha="right", fontsize=8)
    ax.legend()
    fig.tight_layout()
    save_static_chart(fig, "monthly_hiring_trend.png")


def plot_education_salary(df: pd.DataFrame):
    """Chart 12: Education level vs salary."""
    print("Generating: Education vs Salary...")

    edu_salary = df.groupby("education")["monthly_income"].mean().round(2)
    edu_salary.index = edu_salary.index.map(EDUCATION_LABELS)

    fig, ax = setup_plot("Average Salary by Education Level",
                         "Education Level", "Average Salary ($)")
    bars = ax.bar(edu_salary.index, edu_salary.values, color=PALETTE[3],
                  edgecolor="white", alpha=0.8)

    for bar, val in zip(bars, edu_salary.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                f"${val:,.0f}", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    save_static_chart(fig, "education_salary.png")


def create_interactive_dashboard(df: pd.DataFrame):
    """Create individual interactive HTML charts using Plotly."""
    print("Generating: Interactive HTML Charts...")

    # 1. Attrition by Department (Pie Chart)
    dept_attr = df.groupby("department")["attrition"].apply(
        lambda x: (x == "Yes").sum()
    ).reset_index()
    dept_attr.columns = ["Department", "Attrited"]

    fig1 = px.pie(dept_attr, values="Attrited", names="Department",
                  title="Attrition Distribution by Department",
                  color_discrete_sequence=PALETTE, hole=0.4)
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    save_interactive_chart(fig1, "dashboard_attrition.html")
    print("  [OK] Attrition Dashboard")

    # 2. Salary Distribution (Box Plot)
    fig2 = px.box(df, x="department", y="monthly_income",
                  color="department", title="Salary Distribution by Department",
                  color_discrete_sequence=PALETTE,
                  labels={"department": "Department",
                         "monthly_income": "Monthly Income ($)"})
    fig2.update_layout(showlegend=False, xaxis_tickangle=-45)
    save_interactive_chart(fig2, "dashboard_salary.html")
    print("  [OK] Salary Dashboard")

    # 3. Satisfaction Radar
    sat_avg = df[["job_satisfaction", "environment_satisfaction",
                  "relationship_satisfaction", "work_life_balance"]].mean().round(2)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatterpolar(
        r=sat_avg.values,
        theta=["Job", "Environment", "Relationship", "Work-Life Balance"],
        fill="toself", name="Satisfaction Scores", line_color=PALETTE[0]
    ))
    fig3.update_layout(
        title="Employee Satisfaction Radar",
        polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
        showlegend=False
    )
    save_interactive_chart(fig3, "dashboard_satisfaction.html")
    print("  [OK] Satisfaction Dashboard")

    # 4. Gender Diversity (Stacked Bar)
    dept_gender = df.groupby(["department", "gender"]).size().reset_index(name="count")
    fig4 = px.bar(dept_gender, x="department", y="count", color="gender",
                  title="Gender Distribution by Department",
                  color_discrete_map={"Male": PALETTE[0], "Female": PALETTE[1]},
                  barmode="stack",
                  labels={"department": "Department", "count": "Count"})
    fig4.update_layout(xaxis_tickangle=-45)
    save_interactive_chart(fig4, "dashboard_diversity.html")
    print("  [OK] Diversity Dashboard")

    # 5. Performance Rating Distribution
    perf_dist = df["performance_rating"].value_counts().reset_index()
    perf_dist.columns = ["Rating", "Count"]
    perf_dist["Rating"] = perf_dist["Rating"].map(PERFORMANCE_LABELS)
    fig5 = px.bar(perf_dist, x="Rating", y="Count",
                  title="Performance Rating Distribution", color="Rating",
                  color_discrete_sequence=PALETTE,
                  labels={"Count": "Number of Employees"})
    save_interactive_chart(fig5, "dashboard_performance.html")
    print("  [OK] Performance Dashboard")

    # 6. Salary vs Experience Scatter
    fig6 = px.scatter(
        df.sample(min(500, len(df))),
        x="years_at_company", y="monthly_income",
        color="department", size="age",
        hover_data=["employee_name", "job_role"],
        title="Salary vs Years of Experience",
        color_discrete_sequence=PALETTE,
        labels={"years_at_company": "Years at Company",
                "monthly_income": "Monthly Income ($)"}
    )
    save_interactive_chart(fig6, "dashboard_experience.html")
    print("  [OK] Experience Dashboard")

    print("  All 6 interactive charts saved individually")


def generate_all_charts(df: pd.DataFrame = None):
    """Generate all charts."""
    print_section("Chart Generation")

    if df is None:
        cleaned_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "cleaned", "hr_data_cleaned.csv"
        )
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
        else:
            df = load_raw_data()
            df = standardize_columns(df)

    print(f"Generating charts for {len(df):,} employees...")

    charts = [
        ("Employee Distribution", plot_employee_distribution),
        ("Gender Diversity", plot_gender_diversity),
        ("Attrition Rate", plot_attrition_rate),
        ("Salary Distribution", plot_salary_distribution),
        ("Age Distribution", plot_age_distribution),
        ("Satisfaction Scores", plot_satisfaction_scores),
        ("Performance vs Salary", plot_performance_vs_salary),
        ("Overtime Impact", plot_overtime_impact),
        ("Promotion Analysis", plot_promotion_analysis),
        ("Correlation Heatmap", plot_correlation_heatmap),
        ("Monthly Hiring Trend", plot_monthly_trend),
        ("Education vs Salary", plot_education_salary)
    ]

    for name, func in charts:
        try:
            func(df)
            print(f"  [OK] {name}")
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")

    # Generate interactive dashboard
    try:
        create_interactive_dashboard(df)
        print(f"  [OK] Interactive Dashboard")
    except Exception as e:
        print(f"  [ERROR] Interactive Dashboard: {e}")

    print(f"\nCharts saved to: {CHARTS_STATIC_DIR}")
    print(f"Interactive dashboard saved to: {REPORTS_HTML_DIR}")


if __name__ == "__main__":
    generate_all_charts()
