#!/usr/bin/env python3
"""
HR Analytics Interactive Dashboard
===================================
Streamlit-based interactive dashboard for HR analytics.
Visualizes KPIs, charts, and insights on a single page.

Usage:
    streamlit run python/dashboard.py
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit not installed. Install with: pip install streamlit")

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from analytics_utils import (
    load_raw_data, load_cleaned_data, calculate_kpis, print_section,
    DATA_CLEANED_DIR, SATISFACTION_LABELS, PERFORMANCE_LABELS,
    EDUCATION_LABELS, get_age_group
)


def load_data():
    """Load and cache data."""
    cleaned_path = os.path.join(DATA_CLEANED_DIR, "hr_data_cleaned.csv")
    if os.path.exists(cleaned_path):
        df = pd.read_csv(cleaned_path)
    else:
        df = load_raw_data()

    # Add derived columns
    df["age_group"] = df["age"].apply(get_age_group)
    return df


def create_dashboard():
    """Main dashboard function."""
    if not STREAMLIT_AVAILABLE:
        print("ERROR: Streamlit is required. Run: pip install streamlit")
        return

    st.set_page_config(
        page_title="HR Analytics Dashboard",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load data
    df = load_data()
    kpis = calculate_kpis(df)

    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/96/bar-chart.png", width=80)
    st.sidebar.title("HR Analytics")
    st.sidebar.markdown("---")

    # Filters
    st.sidebar.subheader("Filters")
    departments = ["All"] + sorted(df["department"].unique().tolist())
    selected_dept = st.sidebar.selectbox("Department", departments)

    genders = ["All"] + sorted(df["gender"].unique().tolist())
    selected_gender = st.sidebar.selectbox("Gender", genders)

    attrition_filter = st.sidebar.radio("Attrition Status", ["All", "Active", "Attrited"])

    # Apply filters
    filtered_df = df.copy()
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df["department"] == selected_dept]
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["gender"] == selected_gender]
    if attrition_filter == "Active":
        filtered_df = filtered_df[filtered_df["attrition"] == "No"]
    elif attrition_filter == "Attrited":
        filtered_df = filtered_df[filtered_df["attrition"] == "Yes"]

    st.sidebar.markdown("---")
    st.sidebar.info(
        "This dashboard provides comprehensive HR analytics "
        "including workforce demographics, attrition analysis, "
        "salary distribution, and employee satisfaction metrics."
    )

    # Main content
    st.title(" HR Analytics Dashboard")
    st.markdown(f"*Dataset: {len(df):,} employees | "
                f"Filtered: {len(filtered_df):,} employees*")

    # KPI Cards
    st.subheader("Key Performance Indicators")
    kpi_cols = st.columns(5)

    with kpi_cols[0]:
        st.metric("Total Employees", f"{kpis['total_employees']:,}",
                  f"{kpis['active_employees']:,} Active")
    with kpi_cols[1]:
        st.metric("Attrition Rate", f"{kpis['attrition_rate']:.1f}%",
                  f"{kpis['attrited_employees']:,} Left")
    with kpi_cols[2]:
        st.metric("Avg Salary", f"${kpis['avg_salary']:,.0f}",
                  f"Median: ${kpis['median_salary']:,.0f}")
    with kpi_cols[3]:
        st.metric("Avg Age", f"{kpis['avg_age']:.1f} yrs",
                  f"Tenure: {kpis['avg_tenure']:.1f} yrs")
    with kpi_cols[4]:
        st.metric("Avg Satisfaction", f"{kpis['avg_job_satisfaction']:.2f}/4",
                  f"WLB: {kpis['avg_work_life_balance']:.2f}/4")

    # Charts
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", "Attrition", "Salary", "Performance", "Diversity"
    ])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Department Distribution")
            dept_counts = filtered_df["department"].value_counts()
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            bars = ax1.bar(dept_counts.index, dept_counts.values,
                          color="#2563EB", edgecolor="white")
            ax1.set_xlabel("Department")
            ax1.set_ylabel("Count")
            ax1.tick_params(axis="x", rotation=45)
            for bar, val in zip(bars, dept_counts.values):
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        str(val), ha="center", va="bottom", fontsize=9)
            fig1.tight_layout()
            st.pyplot(fig1)

        with col2:
            st.subheader("Gender Distribution")
            gender_counts = filtered_df["gender"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            colors = ["#2563EB", "#7C3AED"]
            ax2.pie(gender_counts.values, labels=gender_counts.index,
                   autopct="%1.1f%%", colors=colors, startangle=90,
                   wedgeprops={"edgecolor": "white", "linewidth": 2})
            ax2.axis("equal")
            st.pyplot(fig2)

        with st.container():
            st.subheader("Age Distribution")
            fig3, ax3 = plt.subplots(figsize=(12, 5))
            ax3.hist(filtered_df["age"], bins=15, color="#2563EB",
                    edgecolor="white", alpha=0.8)
            ax3.axvline(filtered_df["age"].mean(), color="#EF4444",
                       linestyle="--", linewidth=2, label="Mean Age")
            ax3.axvline(filtered_df["age"].median(), color="#10B981",
                       linestyle=":", linewidth=2, label="Median Age")
            ax3.set_xlabel("Age")
            ax3.set_ylabel("Count")
            ax3.legend()
            st.pyplot(fig3)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Attrition by Department")
            dept_attr = filtered_df.groupby("department")["attrition"].apply(
                lambda x: (x == "Yes").mean() * 100
            ).sort_values(ascending=True)
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            colors_attr = ["#EF4444" if v > 20 else "#F59E0B" if v > 15 else "#10B981"
                          for v in dept_attr.values]
            ax4.barh(dept_attr.index, dept_attr.values, color=colors_attr,
                    edgecolor="white")
            ax4.set_xlabel("Attrition Rate (%)")
            for i, v in enumerate(dept_attr.values):
                ax4.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)
            st.pyplot(fig4)

        with col2:
            st.subheader("Attrition by Factor")
            factors = ["gender", "overtime", "marital_status", "job_level"]
            fig5, axes = plt.subplots(2, 2, figsize=(12, 10))
            axes = axes.flatten()

            for idx, factor in enumerate(factors):
                factor_attr = filtered_df.groupby(factor)["attrition"].apply(
                    lambda x: (x == "Yes").mean() * 100
                )
                axes[idx].bar(factor_attr.index.astype(str), factor_attr.values,
                            color="#2563EB", edgecolor="white")
                axes[idx].set_title(f"Attrition by {factor.replace('_', ' ').title()}")
                axes[idx].set_ylabel("Attrition Rate (%)")
                axes[idx].tick_params(axis="x", rotation=45)

            fig5.tight_layout()
            st.pyplot(fig5)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Salary by Department")
            dept_sal = filtered_df.groupby("department")["monthly_income"].mean().sort_values()
            fig6, ax6 = plt.subplots(figsize=(10, 6))
            ax6.barh(dept_sal.index, dept_sal.values, color="#10B981",
                    edgecolor="white")
            ax6.set_xlabel("Average Monthly Salary ($)")
            ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
            for i, v in enumerate(dept_sal.values):
                ax6.text(v + 100, i, f"${v:,.0f}", va="center", fontsize=8)
            st.pyplot(fig6)

        with col2:
            st.subheader("Salary vs Performance")
            fig7, ax7 = plt.subplots(figsize=(10, 6))
            scatter = ax7.scatter(
                filtered_df["performance_rating"],
                filtered_df["monthly_income"],
                c=filtered_df["age"], cmap="viridis",
                alpha=0.6, s=30
            )
            ax7.set_xlabel("Performance Rating")
            ax7.set_ylabel("Monthly Income ($)")
            plt.colorbar(scatter, ax=ax7, label="Age")
            st.pyplot(fig7)

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Performance Distribution")
            perf_counts = filtered_df["performance_rating"].value_counts().sort_index()
            perf_labels = [PERFORMANCE_LABELS.get(r, str(r))
                          for r in perf_counts.index]
            fig8, ax8 = plt.subplots(figsize=(8, 6))
            ax8.pie(perf_counts.values, labels=perf_labels,
                   autopct="%1.1f%%", colors=["#EF4444", "#F59E0B", "#2563EB", "#10B981"],
                   startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2})
            ax8.axis("equal")
            st.pyplot(fig8)

        with col2:
            st.subheader("Satisfaction Scores")
            sat_cols = ["job_satisfaction", "environment_satisfaction",
                       "relationship_satisfaction", "work_life_balance"]
            sat_means = filtered_df[sat_cols].mean()
            sat_labels = ["Job", "Environment", "Relationship", "WLB"]
            fig9, ax9 = plt.subplots(figsize=(8, 6))
            bars = ax9.bar(sat_labels, sat_means.values,
                          color=["#2563EB", "#7C3AED", "#10B981", "#F59E0B"],
                          edgecolor="white", width=0.6)
            ax9.set_ylabel("Score (1-4)")
            ax9.set_ylim(0, 4.5)
            for bar, val in zip(bars, sat_means.values):
                ax9.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                        f"{val:.2f}", ha="center", va="bottom", fontweight="bold")
            st.pyplot(fig9)

    with tab5:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Gender Diversity by Department")
            dept_gender = filtered_df.groupby(["department", "gender"]).size().unstack(fill_value=0)
            fig10, ax10 = plt.subplots(figsize=(12, 6))
            dept_gender.plot(kind="bar", stacked=True, ax=ax10,
                           color=["#2563EB", "#7C3AED"],
                           edgecolor="white")
            ax10.set_xlabel("Department")
            ax10.set_ylabel("Count")
            ax10.tick_params(axis="x", rotation=45)
            ax10.legend(title="Gender")
            fig10.tight_layout()
            st.pyplot(fig10)

        with col2:
            st.subheader("Education Field Distribution")
            edu_counts = filtered_df["education_field"].value_counts()
            fig11, ax11 = plt.subplots(figsize=(10, 6))
            ax11.barh(edu_counts.index, edu_counts.values, color="#7C3AED",
                     edgecolor="white")
            ax11.set_xlabel("Count")
            for i, v in enumerate(edu_counts.values):
                ax11.text(v + 5, i, str(v), va="center", fontsize=9)
            fig11.tight_layout()
            st.pyplot(fig11)

    # Insights section
    st.markdown("---")
    st.subheader(" Key Business Insights")

    insight_cols = st.columns(3)
    with insight_cols[0]:
        st.info(
            f"**Highest Attrition:**\n"
            f"{dept_attr.index[-1] if 'dept_attr' in dir() else 'N/A'} "
            f"has the highest attrition rate. "
            f"Consider retention programs and exit interviews."
        )
    with insight_cols[1]:
        st.info(
            f"**Compensation:**\n"
            f"Average salary is ${kpis['avg_salary']:,.0f}/month. "
            f"{'Below' if kpis['avg_salary'] < 7000 else 'Above'} "
            f"industry benchmarks for this region."
        )
    with insight_cols[2]:
        st.info(
            f"**Diversity:**\n"
            f"{kpis['female_percentage']:.1f}% female representation. "
            f"Consider targeted recruitment to improve gender balance."
        )

    # Data table
    st.markdown("---")
    st.subheader(" Employee Data Preview")
    st.dataframe(
        filtered_df.head(100)[
            ["employee_id", "employee_name", "department", "job_role",
             "monthly_income", "attrition", "job_satisfaction"]
        ],
        use_container_width=True
    )

    st.caption(f"HR Analytics Dashboard | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    if STREAMLIT_AVAILABLE:
        create_dashboard()
    else:
        print("=" * 60)
        print("  HR Analytics Dashboard")
        print("=" * 60)
        print("\nStreamlit is required to run the interactive dashboard.")
        print("\nInstallation:")
        print("  pip install streamlit")
        print("\nRun:")
        print("  streamlit run python/dashboard.py")
        print("\nAlternatively, view the static charts in reports/screenshots/")
