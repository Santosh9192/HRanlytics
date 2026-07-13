#!/usr/bin/env python3
"""
Dashboard Screenshot Generator
===============================
Generates professional dashboard preview images (PNG) for the README.
Creates composite "screenshot-style" images that look like real BI dashboards.

Output files (saved to reports/screenshots/):
  - executive_dashboard.png
  - employee_dashboard.png
  - attrition_dashboard.png
  - salary_dashboard.png
  - diversity_dashboard.png
  - performance_dashboard.png
"""

import pandas as pd
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics_utils import (
    calculate_kpis, PROJECT_ROOT,
    SATISFACTION_LABELS, PERFORMANCE_LABELS, EDUCATION_LABELS,
    get_age_group
)

# Output directory
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── Colour palette ─────────────────────────────────────────────────
C = {
    "bg":       "#0F172A",   # dark bg
    "card":     "#1E293B",   # card bg
    "accent":   "#3B82F6",   # blue accent
    "accent2":  "#8B5CF6",   # purple
    "green":    "#10B981",
    "red":      "#EF4444",
    "amber":    "#F59E0B",
    "cyan":     "#06B6D4",
    "pink":     "#EC4899",
    "white":    "#F8FAFC",
    "muted":    "#94A3B8",
    "border":   "#334155",
    "purple":  "#8B5CF6",
    "orange":  "#F97316",
}

PALETTE = ["#3B82F6", "#8B5CF6", "#10B981", "#EF4444",
           "#F59E0B", "#06B6D4", "#EC4899", "#F97316"]

plt.rcParams.update({
    "figure.facecolor": C["bg"],
    "axes.facecolor": C["card"],
    "axes.edgecolor": C["border"],
    "axes.labelcolor": C["muted"],
    "text.color": C["white"],
    "xtick.color": C["muted"],
    "ytick.color": C["muted"],
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
})


# ── Helpers ────────────────────────────────────────────────────────

def load_data():
    """Load cleaned HR dataset."""
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "cleaned", "hr_data_cleaned.csv"
    )
    df = pd.read_csv(path)
    df["age_group"] = df["age"].apply(get_age_group)
    return df


def add_header(fig, title, subtitle=""):
    """Add a dashboard title bar at the top of the figure."""
    ax = fig.add_axes([0, 0.93, 1, 0.07], facecolor=C["bg"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # App icon and title
    ax.text(0.03, 0.55, "📊", fontsize=22, va="center", transform=ax.transAxes)
    ax.text(0.08, 0.55, title, fontsize=18, fontweight="bold",
            color=C["white"], va="center", transform=ax.transAxes)
    if subtitle:
        ax.text(0.08, 0.15, subtitle, fontsize=10, color=C["muted"],
                va="bottom", transform=ax.transAxes)

    # Right-side meta
    ax.text(0.97, 0.55, "HR Analytics • BI Dashboard", fontsize=9,
            color=C["muted"], ha="right", va="center", transform=ax.transAxes)


def add_footer(fig, text="HR Analytics Dashboard"):
    """Add a footer bar."""
    ax = fig.add_axes([0, 0, 1, 0.035], facecolor=C["bg"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.4, text, fontsize=8, color=C["muted"],
            ha="center", va="center", transform=ax.transAxes)


def kpi_card(ax, label, value, delta="", color=C["accent"]):
    """Draw a single KPI card."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Card background
    card = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                           boxstyle="round,pad=0.05",
                           facecolor=C["card"], edgecolor=C["border"],
                           linewidth=1)
    ax.add_patch(card)

    # Accent line
    ax.axhline(y=0.88, xmin=0.06, xmax=0.94, color=color, linewidth=3)

    # Value
    ax.text(0.5, 0.52, str(value), fontsize=20, fontweight="bold",
            color=C["white"], ha="center", va="center", transform=ax.transAxes)
    # Label
    ax.text(0.5, 0.22, label, fontsize=9, color=C["muted"],
            ha="center", va="center", transform=ax.transAxes)
    # Delta
    if delta:
        ax.text(0.5, 0.08, delta, fontsize=8,
                color=C["green"] if "+" in str(delta) else C["amber"],
                ha="center", va="center", transform=ax.transAxes)


# ═══════════════════════════════════════════════════════════════════
#  1. EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_executive_dashboard(df, kpis):
    """Executive summary / overview dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Executive Dashboard",
               "High-level overview of workforce metrics and KPIs")

    # KPI row (top)
    kpi_data = [
        ("👥", f"{kpis['total_employees']:,}", "Total Employees",
         f"{kpis['active_employees']:,} Active", C["accent"]),
        ("📉", f"{kpis['attrition_rate']:.1f}%", "Attrition Rate",
         f"{kpis['attrited_employees']:,} Left", C["red"]),
        ("💰", f"${kpis['avg_salary']:,.0f}", "Avg Salary",
         f"Median: ${kpis['median_salary']:,.0f}", C["green"]),
        ("📅", f"{kpis['avg_age']:.1f} yrs", "Avg Age",
         f"Tenure: {kpis['avg_tenure']:.1f} yrs", C["amber"]),
        ("⭐", f"{kpis['avg_job_satisfaction']:.2f}", "Avg Satisfaction",
         f"WLB: {kpis['avg_work_life_balance']:.2f}", C["purple"]),
    ]

    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    # Charts: 2x2 grid
    gs = fig.add_gridspec(2, 2, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Top-left: Department distribution ──
    ax1 = fig.add_subplot(gs[0, 0])
    dept_counts = df["department"].value_counts()
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(dept_counts))]
    bars = ax1.barh(dept_counts.index, dept_counts.values,
                    color=colors, edgecolor="none", height=0.6)
    ax1.set_title("Department Distribution", color=C["white"], loc="left")
    ax1.set_xlabel("Count", color=C["muted"])
    for bar, val in zip(bars, dept_counts.values):
        ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=8, color=C["muted"])
    ax1.tick_params(colors=C["muted"], labelsize=8)
    ax1.spines["bottom"].set_color(C["border"])
    ax1.spines["left"].set_color(C["border"])

    # ── Top-right: Gender pie ──
    ax2 = fig.add_subplot(gs[0, 1])
    gender_counts = df["gender"].value_counts()
    wedges, texts, autotexts = ax2.pie(
        gender_counts.values, labels=gender_counts.index,
        autopct="%1.1f%%", colors=[C["accent"], C["accent2"]],
        startangle=90, wedgeprops={"edgecolor": C["card"], "linewidth": 2},
        textprops={"color": C["white"], "fontsize": 9}
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax2.set_title("Gender Distribution", color=C["white"], loc="left",
                  pad=15)

    # ── Bottom-left: Age histogram ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(df["age"], bins=15, color=C["accent"], edgecolor=C["bg"],
             linewidth=0.5, alpha=0.8)
    ax3.axvline(df["age"].mean(), color=C["red"], linestyle="--",
                linewidth=2, label=f"Mean: {df['age'].mean():.1f}")
    ax3.axvline(df["age"].median(), color=C["green"], linestyle=":",
                linewidth=2, label=f"Median: {df['age'].median():.1f}")
    ax3.set_title("Age Distribution", color=C["white"], loc="left")
    ax3.set_xlabel("Age", color=C["muted"])
    ax3.set_ylabel("Count", color=C["muted"])
    ax3.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax3.tick_params(colors=C["muted"], labelsize=8)
    ax3.spines["bottom"].set_color(C["border"])
    ax3.spines["left"].set_color(C["border"])

    # ── Bottom-right: KPIs table ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis("off")
    ax4.set_title("Key Metrics Summary", color=C["white"], loc="left")

    table_data = [
        ["Metric", "Value"],
        ["Active Employees", f"{kpis['active_employees']:,}"],
        ["Attrited Employees", f"{kpis['attrited_employees']:,}"],
        ["Promotion Rate", f"{kpis['promotion_rate']:.1f}%"],
        ["Overtime %", f"{kpis['overtime_percentage']:.1f}%"],
        ["Female %", f"{kpis['female_percentage']:.1f}%"],
        ["Total Salary Budget", f"${kpis['total_salary_budget']:,.0f}"],
        ["Departments", str(kpis['department_count'])],
    ]
    table = ax4.table(
        cellText=table_data[1:],
        colLabels=table_data[0],
        cellLoc="center",
        loc="center",
        cellColours=[
            [C["card"], C["card"]] for _ in range(len(table_data) - 1)
        ],
        colColours=[C["accent"], C["accent2"]],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.6)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(C["border"])
        cell.set_text_props(color=C["white"] if r > 0 else "white")

    add_footer(fig, "Executive Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "executive_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  2. EMPLOYEE DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_employee_dashboard(df, kpis):
    """Employee demographics dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Employee Dashboard",
               "Workforce demographics, education, and employee details")

    # KPI row
    kpi_data = [
        ("👥", f"{kpis['total_employees']:,}", "Total Employees",
         f"{df['department'].nunique()} Depts", C["accent"]),
        ("👩", f"{kpis['female_percentage']:.1f}%", "Female Workforce",
         f"{kpis['female_count']:,} Women", C["accent2"]),
        ("🎓", f"{df['education'].nunique()} Levels", "Education Diversity",
         f"{df['education_field'].nunique()} Fields", C["green"]),
        ("🏙️", f"{df['city'].nunique()}", "Cities",
         f"{df['state'].nunique()} States", C["amber"]),
        ("📋", f"{df['job_role'].nunique()}", "Job Roles",
         f"{df['job_level'].max()} Levels", C["cyan"]),
    ]
    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    gs = fig.add_gridspec(2, 3, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Education field distribution ──
    ax1 = fig.add_subplot(gs[0, 0])
    edu_counts = df["education_field"].value_counts()
    ax1.barh(edu_counts.index, edu_counts.values, color=PALETTE,
             edgecolor="none", height=0.6)
    ax1.set_title("Education Field", color=C["white"], loc="left")
    ax1.set_xlabel("Count", color=C["muted"])
    ax1.tick_params(colors=C["muted"], labelsize=8)
    ax1.spines["bottom"].set_color(C["border"])
    ax1.spines["left"].set_color(C["border"])
    for i, v in enumerate(edu_counts.values):
        ax1.text(v + 5, i, str(v), va="center", fontsize=8, color=C["muted"])

    # ── Job role distribution ──
    ax2 = fig.add_subplot(gs[0, 1])
    role_counts = df["job_role"].value_counts().head(10)
    ax2.barh(role_counts.index, role_counts.values, color=PALETTE[0],
             edgecolor="none", height=0.6)
    ax2.set_title("Top 10 Job Roles", color=C["white"], loc="left")
    ax2.tick_params(colors=C["muted"], labelsize=8)
    ax2.spines["bottom"].set_color(C["border"])
    ax2.spines["left"].set_color(C["border"])
    for i, v in enumerate(role_counts.values):
        ax2.text(v + 5, i, str(v), va="center", fontsize=8, color=C["muted"])

    # ── Marital status ──
    ax3 = fig.add_subplot(gs[0, 2])
    ms_counts = df["marital_status"].value_counts()
    wedges, texts, autotexts = ax3.pie(
        ms_counts.values, labels=ms_counts.index,
        autopct="%1.1f%%", colors=[C["accent"], C["green"], C["amber"]],
        startangle=90, wedgeprops={"edgecolor": C["card"], "linewidth": 2},
        textprops={"color": C["white"], "fontsize": 9}
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax3.set_title("Marital Status", color=C["white"], loc="left", pad=15)

    # ── Age group distribution ──
    ax4 = fig.add_subplot(gs[1, 0])
    age_groups = df.groupby("age_group", observed=True).size()
    ax4.bar(age_groups.index, age_groups.values, color=PALETTE[4:],
            edgecolor="none", width=0.6)
    ax4.set_title("Age Groups", color=C["white"], loc="left")
    ax4.set_ylabel("Count", color=C["muted"])
    ax4.tick_params(colors=C["muted"], labelsize=8)
    ax4.spines["bottom"].set_color(C["border"])
    ax4.spines["left"].set_color(C["border"])
    for i, (k, v) in enumerate(age_groups.items()):
        ax4.text(i, v + 10, str(v), ha="center", fontsize=9,
                 color=C["muted"], fontweight="bold")

    # ── Business travel ──
    ax5 = fig.add_subplot(gs[1, 1])
    travel_counts = df["business_travel"].value_counts()
    ax5.bar(travel_counts.index, travel_counts.values, color=PALETTE[1:4],
            edgecolor="none", width=0.5)
    ax5.set_title("Business Travel", color=C["white"], loc="left")
    ax5.tick_params(colors=C["muted"], labelsize=8)
    ax5.spines["bottom"].set_color(C["border"])
    ax5.spines["left"].set_color(C["border"])
    for i, (k, v) in enumerate(travel_counts.items()):
        ax5.text(i, v + 10, str(v), ha="center", fontsize=9,
                 color=C["muted"], fontweight="bold")

    # ── Job level distribution ──
    ax6 = fig.add_subplot(gs[1, 2])
    jl_counts = df["job_level"].value_counts().sort_index()
    ax6.bar(jl_counts.index.astype(str), jl_counts.values,
            color=PALETTE[0], edgecolor="none", width=0.5)
    ax6.set_title("Job Level Distribution", color=C["white"], loc="left")
    ax6.set_xlabel("Level", color=C["muted"])
    ax6.set_ylabel("Count", color=C["muted"])
    ax6.tick_params(colors=C["muted"], labelsize=8)
    ax6.spines["bottom"].set_color(C["border"])
    ax6.spines["left"].set_color(C["border"])
    for i, v in enumerate(jl_counts.values):
        ax6.text(i, v + 10, str(v), ha="center", fontsize=9,
                 color=C["muted"], fontweight="bold")

    add_footer(fig, "Employee Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "employee_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  3. ATTRITION DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_attrition_dashboard(df, kpis):
    """Attrition analysis dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Attrition Dashboard",
               "Employee turnover analysis and retention insights")

    # KPI row
    kpi_data = [
        ("📉", f"{kpis['attrition_rate']:.1f}%", "Attrition Rate",
         f"{kpis['attrited_employees']:,} Left", C["red"]),
        ("🟢", f"{kpis['active_employees']:,}", "Active Employees",
         f"Retention: {(1 - kpis['attrition_rate']/100)*100:.1f}%", C["green"]),
        ("💼", f"{df[df['attrition']=='Yes']['monthly_income'].mean():,.0f}",
         "Avg Salary (Left)", "vs Active", C["amber"]),
        ("😊", f"{df[df['attrition']=='Yes']['job_satisfaction'].mean():.2f}/4",
         "Satisfaction (Left)", "vs Active", C["orange"]),
        ("⏰", f"{kpis['overtime_percentage']:.1f}%", "Overtime %",
         "Key attrition factor", C["pink"]),
    ]
    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    gs = fig.add_gridspec(2, 2, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Attrition by department ──
    ax1 = fig.add_subplot(gs[0, 0])
    dept_attr = df.groupby("department")["attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=True)
    colors = [C["red"] if v > 20 else C["amber"] if v > 15 else C["green"]
              for v in dept_attr.values]
    bars = ax1.barh(dept_attr.index, dept_attr.values, color=colors,
                    edgecolor="none", height=0.6)
    ax1.set_title("Attrition Rate by Department (%)", color=C["white"],
                  loc="left")
    ax1.set_xlabel("Attrition Rate (%)", color=C["muted"])
    ax1.tick_params(colors=C["muted"], labelsize=8)
    ax1.spines["bottom"].set_color(C["border"])
    ax1.spines["left"].set_color(C["border"])
    for bar, val in zip(bars, dept_attr.values):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=8, color=C["muted"],
                fontweight="bold")

    # ── Attrition by factors ──
    ax2 = fig.add_subplot(gs[0, 1])
    factors_data = {}
    for factor in ["overtime", "marital_status", "business_travel"]:
        f_attr = df.groupby(factor)["attrition"].apply(
            lambda x: (x == "Yes").mean() * 100
        )
        for k, v in f_attr.items():
            factors_data[f"{factor}\n({k})"] = v
    f_sorted = dict(sorted(factors_data.items(), key=lambda x: x[1]))
    colors_f = [C["red"] if v > 20 else C["amber"] for v in f_sorted.values()]
    ax2.barh(list(f_sorted.keys()), list(f_sorted.values()),
             color=colors_f, edgecolor="none", height=0.6)
    ax2.set_title("Attrition by Factors (%)", color=C["white"], loc="left")
    ax2.tick_params(colors=C["muted"], labelsize=7)
    ax2.spines["bottom"].set_color(C["border"])
    ax2.spines["left"].set_color(C["border"])

    # ── Attrited vs Active comparison ──
    ax3 = fig.add_subplot(gs[1, 0])
    attrited = df[df["attrition"] == "Yes"]
    active = df[df["attrition"] == "No"]
    metrics = ["age", "monthly_income", "years_at_company",
               "job_satisfaction", "work_life_balance",
               "years_since_last_promotion"]
    labels_m = ["Age", "Income", "Tenure", "Satisfaction",
                "WLB", "Promotion Gap"]
    x = np.arange(len(metrics))
    w = 0.35
    attrited_means = [attrited[m].mean() for m in metrics]
    active_means = [active[m].mean() for m in metrics]
    ax3.bar(x - w/2, attrited_means, w, label="Attrited",
            color=C["red"], alpha=0.8, edgecolor="none")
    ax3.bar(x + w/2, active_means, w, label="Active",
            color=C["green"], alpha=0.8, edgecolor="none")
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels_m, fontsize=8, color=C["muted"])
    ax3.set_title("Attrited vs Active Comparison", color=C["white"], loc="left")
    ax3.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax3.tick_params(colors=C["muted"], labelsize=8)
    ax3.spines["bottom"].set_color(C["border"])
    ax3.spines["left"].set_color(C["border"])

    # ── Attrition by job level & satisfaction ──
    ax4 = fig.add_subplot(gs[1, 1])
    jl_attr = df.groupby("job_level")["attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_index()
    ax4.plot(jl_attr.index, jl_attr.values, color=C["red"], linewidth=2.5,
             marker="o", markersize=8, markerfacecolor=C["red"],
             markeredgecolor="white", markeredgewidth=1.5)
    ax4.fill_between(jl_attr.index, jl_attr.values, alpha=0.15, color=C["red"])
    ax4.set_title("Attrition Rate by Job Level", color=C["white"], loc="left")
    ax4.set_xlabel("Job Level", color=C["muted"])
    ax4.set_ylabel("Attrition Rate (%)", color=C["muted"])
    ax4.set_xticks(jl_attr.index)
    ax4.tick_params(colors=C["muted"], labelsize=8)
    ax4.spines["bottom"].set_color(C["border"])
    ax4.spines["left"].set_color(C["border"])
    for x_val, y_val in zip(jl_attr.index, jl_attr.values):
        ax4.text(x_val, y_val + 1.5, f"{y_val:.1f}%", ha="center",
                 fontsize=8, color=C["muted"], fontweight="bold")

    add_footer(fig, "Attrition Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "attrition_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  4. SALARY DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_salary_dashboard(df, kpis):
    """Salary and compensation dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Salary Dashboard",
               "Compensation analysis, salary distribution, and pay equity")

    # KPI row
    kpi_data = [
        ("💰", f"${kpis['avg_salary']:,.0f}", "Avg Salary",
         f"Median: ${kpis['median_salary']:,.0f}", C["green"]),
        ("📈", f"${kpis['min_salary']:,.0f}", "Min Salary",
         f"Max: ${kpis['max_salary']:,.0f}", C["amber"]),
        ("🏢", f"${kpis['total_salary_budget']:,.0f}", "Total Budget",
         "Monthly payroll", C["accent"]),
        ("📊", f"{df['percent_salary_hike'].mean():.1f}%", "Avg Salary Hike",
         "Annual increase", C["cyan"]),
        ("⚖️", f"{df['stock_option_level'].mean():.1f}", "Avg Stock Level",
         "Equity compensation", C["purple"]),
    ]
    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    gs = fig.add_gridspec(2, 2, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Salary by department ──
    ax1 = fig.add_subplot(gs[0, 0])
    dept_sal = df.groupby("department")["monthly_income"].mean().sort_values()
    bars = ax1.barh(dept_sal.index, dept_sal.values, color=PALETTE[2],
                    edgecolor="none", height=0.6)
    ax1.set_title("Average Salary by Department", color=C["white"], loc="left")
    ax1.set_xlabel("Monthly Income ($)", color=C["muted"])
    ax1.tick_params(colors=C["muted"], labelsize=8)
    ax1.spines["bottom"].set_color(C["border"])
    ax1.spines["left"].set_color(C["border"])
    for bar, val in zip(bars, dept_sal.values):
        ax1.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                f"${val:,.0f}", va="center", fontsize=7,
                color=C["muted"], fontweight="bold")
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    # ── Salary vs Performance scatter ──
    ax2 = fig.add_subplot(gs[0, 1])
    sample = df.sample(min(800, len(df)))
    scatter = ax2.scatter(
        sample["performance_rating"],
        sample["monthly_income"],
        c=sample["age"], cmap="plasma",
        alpha=0.6, s=25, edgecolors="none"
    )
    ax2.set_title("Salary vs Performance", color=C["white"], loc="left")
    ax2.set_xlabel("Performance Rating", color=C["muted"])
    ax2.set_ylabel("Monthly Income ($)", color=C["muted"])
    cbar = plt.colorbar(scatter, ax=ax2, label="Age")
    cbar.ax.yaxis.label.set_color(C["muted"])
    cbar.ax.tick_params(colors=C["muted"])
    ax2.tick_params(colors=C["muted"], labelsize=8)
    ax2.spines["bottom"].set_color(C["border"])
    ax2.spines["left"].set_color(C["border"])

    # ── Salary by education ──
    ax3 = fig.add_subplot(gs[1, 0])
    edu_sal = df.groupby("education", observed=True)["monthly_income"].mean().round(2)
    edu_sal.index = edu_sal.index.map(EDUCATION_LABELS)
    bars = ax3.bar(edu_sal.index, edu_sal.values,
                   color=[PALETTE[i % len(PALETTE)] for i in range(len(edu_sal))],
                   edgecolor="none", width=0.6)
    ax3.set_title("Salary by Education Level", color=C["white"], loc="left")
    ax3.set_ylabel("Monthly Income ($)", color=C["muted"])
    ax3.tick_params(colors=C["muted"], labelsize=8)
    ax3.spines["bottom"].set_color(C["border"])
    ax3.spines["left"].set_color(C["border"])
    for bar, val in zip(bars, edu_sal.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f"${val:,.0f}", ha="center", fontsize=8,
                color=C["muted"], fontweight="bold")
    plt.setp(ax3.get_xticklabels(), rotation=30, ha="right")

    # ── Gender pay gap ──
    ax4 = fig.add_subplot(gs[1, 1])
    gender_pay = df.groupby(["department", "gender"])["monthly_income"].mean().unstack()
    gender_pay.plot(kind="bar", ax=ax4, color=[C["accent"], C["accent2"]],
                    edgecolor="none", width=0.7)
    ax4.set_title("Gender Pay Gap by Department", color=C["white"], loc="left")
    ax4.set_ylabel("Monthly Income ($)", color=C["muted"])
    ax4.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax4.tick_params(colors=C["muted"], labelsize=7)
    ax4.spines["bottom"].set_color(C["border"])
    ax4.spines["left"].set_color(C["border"])
    plt.setp(ax4.get_xticklabels(), rotation=45, ha="right")

    add_footer(fig, "Salary Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "salary_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  5. DIVERSITY DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_diversity_dashboard(df, kpis):
    """Diversity and inclusion dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Diversity Dashboard",
               "Workforce diversity, inclusion metrics, and demographic analysis")

    # KPI row
    kpi_data = [
        ("👩", f"{kpis['female_percentage']:.1f}%", "Female Workforce",
         f"{kpis['female_count']:,} Women", C["accent2"]),
        ("👨", f"{100 - kpis['female_percentage']:.1f}%", "Male Workforce",
         f"{kpis['male_count']:,} Men", C["accent"]),
        ("🎓", f"{df['education_field'].nunique()}", "Education Fields",
         f"5 Education Levels", C["green"]),
        ("🏙️", f"{df['city'].nunique()}", "Unique Cities",
         f"Across {df['state'].nunique()} states", C["amber"]),
        ("⚖️", f"{df['marital_status'].nunique()}", "Demographics",
         "Diverse workforce", C["cyan"]),
    ]
    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    gs = fig.add_gridspec(2, 3, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Gender by department (stacked) ──
    ax1 = fig.add_subplot(gs[0, 0])
    dept_gender = df.groupby(["department", "gender"]).size().unstack(fill_value=0)
    dept_gender.plot(kind="bar", stacked=True, ax=ax1,
                     color=[C["accent"], C["accent2"]],
                     edgecolor=C["bg"], linewidth=0.5)
    ax1.set_title("Gender by Department", color=C["white"], loc="left")
    ax1.set_ylabel("Count", color=C["muted"])
    ax1.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax1.tick_params(colors=C["muted"], labelsize=7)
    ax1.spines["bottom"].set_color(C["border"])
    ax1.spines["left"].set_color(C["border"])
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

    # ── Overall gender ──
    ax2 = fig.add_subplot(gs[0, 1])
    gender_counts = df["gender"].value_counts()
    wedges, texts, autotexts = ax2.pie(
        gender_counts.values, labels=gender_counts.index,
        autopct="%1.1f%%", colors=[C["accent"], C["accent2"]],
        startangle=90, wedgeprops={"edgecolor": C["card"], "linewidth": 2},
        textprops={"color": C["white"], "fontsize": 10}
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax2.set_title("Gender Diversity", color=C["white"], loc="left", pad=15)

    # ── Education field diversity ──
    ax3 = fig.add_subplot(gs[0, 2])
    edu_counts = df["education_field"].value_counts()
    wedges, texts, autotexts = ax3.pie(
        edu_counts.values, labels=edu_counts.index,
        autopct="%1.1f%%", colors=PALETTE,
        startangle=90, wedgeprops={"edgecolor": C["card"], "linewidth": 2},
        textprops={"color": C["white"], "fontsize": 8}
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax3.set_title("Education Field", color=C["white"], loc="left", pad=15)

    # ── Diversity by job level ──
    ax4 = fig.add_subplot(gs[1, 0])
    jl_gender = df.groupby(["job_level", "gender"]).size().unstack(fill_value=0)
    jl_gender.plot(kind="bar", stacked=True, ax=ax4,
                   color=[C["accent"], C["accent2"]],
                   edgecolor=C["bg"], linewidth=0.5)
    ax4.set_title("Gender by Job Level", color=C["white"], loc="left")
    ax4.set_xlabel("Job Level", color=C["muted"])
    ax4.set_ylabel("Count", color=C["muted"])
    ax4.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax4.tick_params(colors=C["muted"], labelsize=8)
    ax4.spines["bottom"].set_color(C["border"])
    ax4.spines["left"].set_color(C["border"])

    # ── Age group diversity ──
    ax5 = fig.add_subplot(gs[1, 1])
    age_gender = df.groupby(["age_group", "gender"]).size().unstack(fill_value=0)
    age_gender.plot(kind="bar", stacked=True, ax=ax5,
                    color=[C["accent"], C["accent2"]],
                    edgecolor=C["bg"], linewidth=0.5)
    ax5.set_title("Gender by Age Group", color=C["white"], loc="left")
    ax5.set_xlabel("Age Group", color=C["muted"])
    ax5.set_ylabel("Count", color=C["muted"])
    ax5.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax5.tick_params(colors=C["muted"], labelsize=8)
    ax5.spines["bottom"].set_color(C["border"])
    ax5.spines["left"].set_color(C["border"])

    # ── Marital status by gender ──
    ax6 = fig.add_subplot(gs[1, 2])
    ms_gender = df.groupby(["marital_status", "gender"]).size().unstack(fill_value=0)
    ms_gender.plot(kind="bar", stacked=True, ax=ax6,
                   color=[C["accent"], C["accent2"]],
                   edgecolor=C["bg"], linewidth=0.5)
    ax6.set_title("Marital Status by Gender", color=C["white"], loc="left")
    ax6.set_xlabel("Status", color=C["muted"])
    ax6.set_ylabel("Count", color=C["muted"])
    ax6.legend(fontsize=8, facecolor=C["card"], edgecolor=C["border"],
               labelcolor=C["white"])
    ax6.tick_params(colors=C["muted"], labelsize=8)
    ax6.spines["bottom"].set_color(C["border"])
    ax6.spines["left"].set_color(C["border"])

    add_footer(fig, "Diversity Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "diversity_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  6. PERFORMANCE DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def generate_performance_dashboard(df, kpis):
    """Performance and satisfaction dashboard."""
    fig = plt.figure(figsize=(18, 10))
    add_header(fig, "Performance Dashboard",
               "Employee performance, satisfaction, and training analysis")

    # KPI row
    perf_avg = df["performance_rating"].mean()
    kpi_data = [
        ("⭐", f"{perf_avg:.2f}/4", "Avg Performance",
         f"Excellent: {len(df[df['performance_rating'] == 4]):,}", C["accent"]),
        ("😊", f"{kpis['avg_job_satisfaction']:.2f}/4", "Job Satisfaction",
         f"High: {len(df[df['job_satisfaction'] >= 3]):,} emp", C["green"]),
        ("⚖️", f"{kpis['avg_work_life_balance']:.2f}/4", "Work-Life Balance",
         f"Score: {kpis['avg_work_life_balance']:.2f}", C["cyan"]),
        ("📚", f"{kpis['avg_training_hours']:.1f}", "Avg Training",
         f"Total sessions: {df['training_times_last_year'].sum():,}", C["amber"]),
        ("📈", f"{df['percent_salary_hike'].mean():.1f}%", "Salary Hike",
         f"Performance linked", C["pink"]),
    ]
    for i, (icon, val, lbl, delta, clr) in enumerate(kpi_data):
        ax = fig.add_axes([0.02 + i * 0.19, 0.78, 0.18, 0.13])
        kpi_card(ax, lbl, f"{icon} {val}", delta, clr)

    gs = fig.add_gridspec(2, 3, left=0.04, right=0.96, top=0.73,
                          bottom=0.06, hspace=0.35, wspace=0.3)

    # ── Performance distribution ──
    ax1 = fig.add_subplot(gs[0, 0])
    perf_counts = df["performance_rating"].value_counts().sort_index()
    perf_labels = [PERFORMANCE_LABELS.get(r, str(r)) for r in perf_counts.index]
    colors_perf = [C["red"], C["amber"], C["accent"], C["green"]]
    wedges, texts, autotexts = ax1.pie(
        perf_counts.values, labels=perf_labels, autopct="%1.1f%%",
        colors=colors_perf, startangle=90,
        wedgeprops={"edgecolor": C["card"], "linewidth": 2},
        textprops={"color": C["white"], "fontsize": 9}
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax1.set_title("Performance Distribution", color=C["white"], loc="left",
                  pad=15)

    # ── Satisfaction scores ──
    ax2 = fig.add_subplot(gs[0, 1])
    sat_cols = ["job_satisfaction", "environment_satisfaction",
                "relationship_satisfaction", "work_life_balance"]
    sat_means = df[sat_cols].mean()
    sat_labels = ["Job", "Environment", "Relationship", "WLB"]
    sat_colors = [C["accent"], C["green"], C["amber"], C["cyan"]]
    bars = ax2.bar(sat_labels, sat_means.values, color=sat_colors,
                   edgecolor="none", width=0.6)
    ax2.set_title("Satisfaction Scores", color=C["white"], loc="left")
    ax2.set_ylabel("Score (1-4)", color=C["muted"])
    ax2.set_ylim(0, 4.5)
    ax2.tick_params(colors=C["muted"], labelsize=9)
    ax2.spines["bottom"].set_color(C["border"])
    ax2.spines["left"].set_color(C["border"])
    for bar, val in zip(bars, sat_means.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{val:.2f}", ha="center", va="bottom", fontsize=9,
                color=C["white"], fontweight="bold")

    # ── Training vs Performance ──
    ax3 = fig.add_subplot(gs[0, 2])
    training_perf = df.groupby("performance_rating", observed=True)[
        "training_times_last_year"
    ].mean()
    tp_labels = [PERFORMANCE_LABELS.get(r, str(r)) for r in training_perf.index]
    ax3.plot(tp_labels, training_perf.values, color=C["accent"],
             linewidth=2.5, marker="o", markersize=8,
             markerfacecolor=C["accent"], markeredgecolor="white",
             markeredgewidth=1.5)
    ax3.fill_between(range(len(training_perf)), training_perf.values,
                     alpha=0.15, color=C["accent"])
    ax3.set_title("Training vs Performance", color=C["white"], loc="left")
    ax3.set_ylabel("Avg Training Sessions", color=C["muted"])
    ax3.tick_params(colors=C["muted"], labelsize=8)
    ax3.spines["bottom"].set_color(C["border"])
    ax3.spines["left"].set_color(C["border"])
    for i, (x, y) in enumerate(zip(tp_labels, training_perf.values)):
        ax3.text(i, y + 0.15, f"{y:.1f}", ha="center", fontsize=9,
                 color=C["muted"], fontweight="bold")

    # ── Performance by department ──
    ax4 = fig.add_subplot(gs[1, 0])
    dept_perf = df.groupby("department")["performance_rating"].mean().sort_values()
    bars = ax4.barh(dept_perf.index, dept_perf.values,
                    color=[PALETTE[i % len(PALETTE)] for i in range(len(dept_perf))],
                    edgecolor="none", height=0.6)
    ax4.set_title("Performance by Department", color=C["white"], loc="left")
    ax4.set_xlabel("Avg Performance Rating", color=C["muted"])
    ax4.tick_params(colors=C["muted"], labelsize=8)
    ax4.spines["bottom"].set_color(C["border"])
    ax4.spines["left"].set_color(C["border"])
    ax4.set_xlim(0, 4.5)
    for bar, val in zip(bars, dept_perf.values):
        ax4.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}", va="center", fontsize=8,
                color=C["muted"], fontweight="bold")

    # ── Salary hike by performance ──
    ax5 = fig.add_subplot(gs[1, 1])
    hike_perf = df.groupby("performance_rating", observed=True)[
        "percent_salary_hike"
    ].mean()
    hp_labels = [PERFORMANCE_LABELS.get(r, str(r)) for r in hike_perf.index]
    bars = ax5.bar(hp_labels, hike_perf.values,
                   color=[PALETTE[i % len(PALETTE)] for i in range(len(hike_perf))],
                   edgecolor="none", width=0.6)
    ax5.set_title("Salary Hike by Performance", color=C["white"], loc="left")
    ax5.set_ylabel("Avg Hike (%)", color=C["muted"])
    ax5.tick_params(colors=C["muted"], labelsize=8)
    ax5.spines["bottom"].set_color(C["border"])
    ax5.spines["left"].set_color(C["border"])
    for bar, val in zip(bars, hike_perf.values):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{val:.1f}%", ha="center", fontsize=9,
                color=C["muted"], fontweight="bold")
    plt.setp(ax5.get_xticklabels(), rotation=20, ha="right")

    # ── Satisfaction heatmap-style bars ──
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis("off")
    ax6.set_title("Satisfaction Distribution", color=C["white"], loc="left")

    # Create a small table showing satisfaction distribution
    sat_dist = df["job_satisfaction"].value_counts().sort_index()
    sat_dist_labels = [SATISFACTION_LABELS.get(r, str(r)) for r in sat_dist.index]
    table_data = [["Level", "Count", "%"]] + [
        [lbl, f"{cnt:,}", f"{cnt/len(df)*100:.1f}%"]
        for lbl, cnt in zip(sat_dist_labels, sat_dist.values)
    ]
    table = ax6.table(
        cellText=table_data[1:],
        colLabels=table_data[0],
        cellLoc="center",
        loc="center",
        cellColours=[
            [C["card"], C["card"], C["card"]] for _ in range(len(table_data) - 1)
        ],
        colColours=[C["accent"], C["green"], C["amber"]],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(C["border"])
        cell.set_text_props(color=C["white"] if r > 0 else "white")

    add_footer(fig, "Performance Dashboard • HR Analytics")
    save_path = os.path.join(SCREENSHOTS_DIR, "performance_dashboard.png")
    fig.savefig(save_path, dpi=180, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"[SAVED] {save_path}")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def generate_all_dashboards():
    """Generate all 6 dashboard screenshot images."""
    print("=" * 60)
    print("  HR Analytics - Dashboard Screenshot Generator")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    try:
        df = load_data()
        kpis = calculate_kpis(df)
        print(f"Loaded {len(df):,} employee records\n")
    except Exception as e:
        print(f"[ERROR] Could not load data: {e}")
        raise

    # Generate each dashboard
    dashboards = [
        ("Executive Dashboard",   generate_executive_dashboard),
        ("Employee Dashboard",    generate_employee_dashboard),
        ("Attrition Dashboard",   generate_attrition_dashboard),
        ("Salary Dashboard",      generate_salary_dashboard),
        ("Diversity Dashboard",   generate_diversity_dashboard),
        ("Performance Dashboard", generate_performance_dashboard),
    ]

    for name, func in dashboards:
        print(f"\n{'-' * 50}")
        print(f"  Generating: {name}")
        try:
            func(df, kpis)
            print(f"  [OK] {name} generated successfully")
        except Exception as e:
            print(f"  [ERROR] Error generating {name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 60}")
    print(f"  All dashboards saved to: {SCREENSHOTS_DIR}")
    print(f"\n  Dashboard images generated:")
    for name, _ in dashboards:
        filename = name.lower().replace(" ", "_") + ".png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        size = os.path.getsize(filepath) / 1024 if os.path.exists(filepath) else 0
        print(f"    [OK] {filename} ({size:.0f} KB)")
    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    generate_all_dashboards()
