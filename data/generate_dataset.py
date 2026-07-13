#!/usr/bin/env python3
"""
HR Analytics Dataset Generator
===============================
Generates a realistic HR dataset of ~5,000 employees with
demographics, compensation, satisfaction, performance, and attrition data.

Outputs:
  - data/raw/hr_data.csv : Raw generated dataset
  - data/raw/hr_data.xlsx : Excel version of raw dataset
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from faker import Faker
import random

# --- Seed for reproducibility ---
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
fake = Faker()
Faker.seed(RANDOM_SEED)

# --- Constants ---
NUM_EMPLOYEES = 5000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Department / Role Configuration ---
DEPARTMENT_ROLES = {
    "Sales": [
        "Sales Executive", "Sales Representative", "Sales Manager",
        "Sales Development Rep", "Account Executive", "Regional Sales Director"
    ],
    "Research & Development": [
        "Research Scientist", "Laboratory Technician", "Research Director",
        "Clinical Research Coordinator", "R&D Manager", "Product Developer"
    ],
    "Human Resources": [
        "HR Executive", "HR Manager", "HR Coordinator",
        "Talent Acquisition Specialist", "Compensation Analyst", "HR Director"
    ],
    "Finance": [
        "Accountant", "Financial Analyst", "Finance Manager",
        "Auditor", "Financial Controller", "CFO"
    ],
    "Information Technology": [
        "Software Engineer", "Data Analyst", "IT Manager",
        "DevOps Engineer", "Systems Administrator", "CTO"
    ],
    "Marketing": [
        "Marketing Executive", "Marketing Manager", "Content Writer",
        "Digital Marketing Specialist", "Brand Manager", "Marketing Director"
    ],
    "Operations": [
        "Operations Analyst", "Operations Manager", "Supply Chain Coordinator",
        "Logistics Specialist", "Facilities Manager", "COO"
    ],
    "Customer Support": [
        "Customer Support Rep", "Support Manager", "Customer Success Manager",
        "Technical Support Engineer", "Quality Assurance Specialist", "Support Director"
    ],
    "Legal": [
        "Legal Advisor", "Corporate Counsel", "Compliance Officer",
        "Legal Secretary", "Paralegal", "General Counsel"
    ],
    "Administration": [
        "Administrative Assistant", "Office Manager", "Executive Assistant",
        "Receptionist", "Administration Director", "Facilities Coordinator"
    ]
}

DEPARTMENTS = list(DEPARTMENT_ROLES.keys())

# --- Education Config ---
EDUCATION_LEVELS = {
    1: "Below College",
    2: "College",
    3: "Bachelor's Degree",
    4: "Master's Degree",
    5: "Doctorate Degree"
}

EDUCATION_FIELDS = [
    "Life Sciences", "Medical", "Marketing", "Technical Degree",
    "Human Resources", "Business Management", "Other", "Engineering",
    "Computer Science", "Finance", "Law", "Arts"
]

# --- Salary Ranges by Job Level (Monthly Income in $) ---
SALARY_RANGES = {
    1: (3000, 6000),
    2: (5000, 9000),
    3: (7000, 13000),
    4: (10000, 18000),
    5: (15000, 25000)
}

# --- Attrition Probability by Department ---
ATTRITION_PROB = {
    "Sales": 0.25,
    "Research & Development": 0.15,
    "Human Resources": 0.20,
    "Finance": 0.12,
    "Information Technology": 0.18,
    "Marketing": 0.22,
    "Operations": 0.16,
    "Customer Support": 0.30,
    "Legal": 0.08,
    "Administration": 0.20
}

FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan", "Jacob",
    "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
    "Brandon", "Benjamin", "Samuel", "Raymond", "Gregory", "Frank", "Alexander",
    "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Nathan",
    "Henry", "Douglas", "Peter", "Adam", "Zachary", "Nathaniel"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Dorothy", "Kimberly", "Emily", "Donna", "Michelle", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Cynthia", "Kathleen", "Angela", "Amy", "Shirley", "Anna", "Brenda",
    "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine",
    "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather",
    "Diane", "Ruth", "Julie", "Olivia", "Joyce", "Virginia", "Victoria",
    "Kelly", "Lauren", "Christina"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
    "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes"
]

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
    ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
    ("Dallas", "TX"), ("Austin", "TX"), ("San Jose", "CA"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("Indianapolis", "IN"),
    ("San Francisco", "CA"), ("Seattle", "WA"), ("Denver", "CO"), ("Nashville", "TN"),
    ("Oklahoma City", "OK"), ("El Paso", "TX"), ("Washington", "DC"), ("Boston", "MA"),
    ("Las Vegas", "NV"), ("Portland", "OR"), ("Memphis", "TN"), ("Louisville", "KY"),
    ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"), ("Tucson", "AZ"),
    ("Fresno", "CA"), ("Sacramento", "CA"), ("Mesa", "AZ"), ("Atlanta", "GA"),
    ("Kansas City", "MO"), ("Omaha", "NE"), ("Colorado Springs", "CO"), ("Raleigh", "NC"),
    ("Long Beach", "CA"), ("Virginia Beach", "VA"), ("Miami", "FL"), ("Oakland", "CA"),
    ("Minneapolis", "MN"), ("Tampa", "FL"), ("Tulsa", "OK"), ("Arlington", "TX"),
    ("New Orleans", "LA"), ("Cleveland", "OH")
]

BUSINESS_TRAVEL_OPTIONS = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
JOB_SATISFACTION_LEVELS = [1, 2, 3, 4]
ENV_SATISFACTION_LEVELS = [1, 2, 3, 4]
RELATIONSHIP_SATISFACTION_LEVELS = [1, 2, 3, 4]
WORK_LIFE_BALANCE_LEVELS = [1, 2, 3, 4]
PERFORMANCE_RATINGS_LIST = [1, 2, 3, 4]
MARITAL_STATUSES = ["Single", "Married", "Divorced"]


# --- Helper Functions ---

def assign_gender(age):
    """Slightly higher male probability for older demographics."""
    base_prob = 0.52
    if age > 45:
        base_prob = 0.55
    return np.random.choice(["Male", "Female"], p=[base_prob, 1 - base_prob])


def generate_name(gender):
    """Generate a realistic full name."""
    first = np.random.choice(
        FIRST_NAMES_MALE if gender == "Male" else FIRST_NAMES_FEMALE
    )
    last = np.random.choice(LAST_NAMES)
    return f"{first} {last}"


def assign_education_field(department):
    """Map department to likely education fields."""
    field_map = {
        "Sales": ["Marketing", "Business Management", "Other"],
        "Research & Development": ["Life Sciences", "Medical", "Engineering", "Technical Degree"],
        "Human Resources": ["Human Resources", "Business Management", "Other"],
        "Finance": ["Finance", "Business Management", "Accounting"],
        "Information Technology": ["Computer Science", "Engineering", "Technical Degree"],
        "Marketing": ["Marketing", "Business Management", "Other"],
        "Operations": ["Business Management", "Engineering", "Other"],
        "Customer Support": ["Other", "Business Management", "Marketing"],
        "Legal": ["Law", "Business Management", "Other"],
        "Administration": ["Other", "Business Management", "Human Resources"]
    }
    return np.random.choice(field_map.get(department, ["Other"]))


def assign_job_level(years_at_company, education_level, age):
    """Determine job level based on experience and education."""
    base = 1
    if years_at_company > 15:
        base += 3
    elif years_at_company > 10:
        base += 2
    elif years_at_company > 5:
        base += 1
    if education_level >= 4:
        base += 1
    if age > 50:
        base += 1
    return min(max(base, 1), 5)


def assign_monthly_income(job_level, department, years_at_company, performance_rating):
    """Calculate a realistic monthly income."""
    low, high = SALARY_RANGES[job_level]
    base = np.random.uniform(low, high)

    # Department premium
    dept_mult = {
        "Information Technology": 1.10, "Finance": 1.08,
        "Legal": 1.12, "Sales": 1.05,
        "Marketing": 1.03, "Operations": 1.02,
        "Research & Development": 1.06, "Human Resources": 1.00,
        "Customer Support": 0.95, "Administration": 0.92
    }
    base *= dept_mult.get(department, 1.0)

    # Years at company bonus
    base += (years_at_company * 150)

    # Performance bonus
    perf_mult = {1: 0.90, 2: 0.95, 3: 1.00, 4: 1.10}
    base *= perf_mult.get(performance_rating, 1.0)

    return round(base, 2)


def assign_years_since_last_promotion(years_at_company, job_level):
    """Realistic years since last promotion distribution."""
    if job_level >= 4:
        return np.random.randint(1, 6)
    elif years_at_company < 2:
        return np.random.randint(0, 2)
    else:
        return np.random.randint(0, min(years_at_company, 8))


def assign_attrition(age, department, job_satisfaction, monthly_income,
                     overtime, years_at_company, performance_rating):
    """Determine attrition probability based on multiple factors."""
    base_prob = ATTRITION_PROB.get(department, 0.15)

    # Age effect: younger employees more likely to leave
    if age < 30:
        base_prob *= 1.5
    elif age > 50:
        base_prob *= 0.5

    # Job satisfaction effect
    sat_mult = {1: 2.0, 2: 1.5, 3: 0.8, 4: 0.5}
    base_prob *= sat_mult.get(job_satisfaction, 1.0)

    # Income effect: lower income -> higher attrition
    if monthly_income < 5000:
        base_prob *= 1.3
    elif monthly_income > 15000:
        base_prob *= 0.6

    # Overtime effect
    if overtime == "Yes":
        base_prob *= 1.4

    # Tenure effect
    if years_at_company < 2:
        base_prob *= 1.3
    elif years_at_company > 10:
        base_prob *= 0.6

    # Performance effect: low performers more likely to leave
    if performance_rating <= 2:
        base_prob *= 1.2

    # Clamp
    base_prob = np.clip(base_prob, 0.05, 0.75)
    return np.random.choice(["Yes", "No"], p=[base_prob, 1 - base_prob])


def generate_employee(eid):
    """Generate a single employee record."""
    age = np.random.randint(22, 62)
    gender = assign_gender(age)
    name = generate_name(gender)

    department = np.random.choice(DEPARTMENTS, p=[
        0.12, 0.18, 0.06, 0.08, 0.15, 0.10, 0.08, 0.12, 0.05, 0.06
    ])

    job_role = np.random.choice(DEPARTMENT_ROLES[department])

    education_level = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.15, 0.40, 0.30, 0.10])
    education_field = assign_education_field(department)
    marital_status = np.random.choice(MARITAL_STATUSES, p=[0.30, 0.55, 0.15])

    years_at_company = max(1, int(np.random.exponential(6)))
    years_at_company = min(years_at_company, age - 21)

    job_level = assign_job_level(years_at_company, education_level, age)
    performance_rating = np.random.choice(PERFORMANCE_RATINGS_LIST, p=[0.10, 0.20, 0.50, 0.20])

    monthly_income = assign_monthly_income(job_level, department, years_at_company, performance_rating)

    years_in_current_role = max(0, min(
        np.random.randint(0, years_at_company + 1), years_at_company
    ))
    years_since_last_promotion = assign_years_since_last_promotion(years_at_company, job_level)
    years_with_current_manager = max(0, min(
        np.random.randint(0, years_in_current_role + 3), years_at_company
    ))

    distance_from_home = np.random.randint(1, 50)
    business_travel = np.random.choice(BUSINESS_TRAVEL_OPTIONS, p=[0.40, 0.40, 0.20])

    overtime = np.random.choice(["Yes", "No"], p=[0.30, 0.70])

    job_satisfaction = np.random.choice(JOB_SATISFACTION_LEVELS, p=[0.10, 0.20, 0.40, 0.30])
    env_satisfaction = np.random.choice(ENV_SATISFACTION_LEVELS, p=[0.10, 0.20, 0.40, 0.30])
    relationship_satisfaction = np.random.choice(RELATIONSHIP_SATISFACTION_LEVELS, p=[0.08, 0.17, 0.40, 0.35])
    work_life_balance = np.random.choice(WORK_LIFE_BALANCE_LEVELS, p=[0.08, 0.22, 0.50, 0.20])

    training_times_last_year = np.random.choice([0, 1, 2, 3, 4, 5, 6],
                                                p=[0.10, 0.15, 0.25, 0.20, 0.15, 0.10, 0.05])
    stock_option_level = np.random.randint(0, 4)
    percent_salary_hike = round(np.random.uniform(8, 25), 1)

    attrition = assign_attrition(
        age, department, job_satisfaction, monthly_income,
        overtime, years_at_company, performance_rating
    )

    # Hire date
    hire_year = max(2000, 2025 - years_at_company - np.random.randint(0, 2))
    hire_month = np.random.randint(1, 13)
    hire_day = np.random.randint(1, 28)
    try:
        hire_date = datetime(hire_year, hire_month, hire_day)
    except ValueError:
        hire_date = datetime(hire_year, 1, 15)

    # Exit date for attrition
    exit_date = None
    if attrition == "Yes":
        exit_years = np.random.randint(1, max(2, years_at_company))
        try:
            exit_date = datetime(
                min(2026, hire_year + exit_years),
                np.random.randint(1, 13),
                np.random.randint(1, 28)
            )
            if exit_date < hire_date:
                exit_date = hire_date + timedelta(days=np.random.randint(30, 365))
            if exit_date > datetime(2026, 6, 30):
                exit_date = datetime(2026, 6, 30)
        except ValueError:
            exit_date = hire_date + timedelta(days=365)

    city_idx = np.random.randint(0, len(CITIES_STATES))
    city, state = CITIES_STATES[city_idx]

    return {
        "EmployeeID": eid,
        "EmployeeName": name,
        "Age": age,
        "Gender": gender,
        "Department": department,
        "JobRole": job_role,
        "Education": education_level,
        "EducationField": education_field,
        "MaritalStatus": marital_status,
        "MonthlyIncome": monthly_income,
        "JobLevel": job_level,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_current_role,
        "YearsSinceLastPromotion": years_since_last_promotion,
        "YearsWithCurrentManager": years_with_current_manager,
        "DistanceFromHome": distance_from_home,
        "BusinessTravel": business_travel,
        "OverTime": overtime,
        "EnvironmentSatisfaction": env_satisfaction,
        "JobSatisfaction": job_satisfaction,
        "RelationshipSatisfaction": relationship_satisfaction,
        "WorkLifeBalance": work_life_balance,
        "PerformanceRating": performance_rating,
        "TrainingTimesLastYear": training_times_last_year,
        "StockOptionLevel": stock_option_level,
        "PercentSalaryHike": percent_salary_hike,
        "Attrition": attrition,
        "HireDate": hire_date.strftime("%Y-%m-%d") if hire_date else "",
        "ExitDate": exit_date.strftime("%Y-%m-%d") if exit_date else "",
        "City": city,
        "State": state,
        "Country": "United States"
    }


def main():
    """Main dataset generation entry point."""
    print("=" * 60)
    print("  HR Analytics Dataset Generator")
    print("=" * 60)

    print(f"\nGenerating {NUM_EMPLOYEES} employee records...")
    records = [generate_employee(i + 1001) for i in range(NUM_EMPLOYEES)]

    df = pd.DataFrame(records)
    print(f"\n[OK] Generated {len(df)} records successfully.")

    # Summary statistics
    print("\n" + "-" * 40)
    print("Dataset Summary:")
    print("-" * 40)
    print(f"  Attrition:   {df['Attrition'].value_counts().get('Yes', 0)} left / "
          f"{df['Attrition'].value_counts().get('No', 0)} stayed")
    print(f"  Departments: {df['Department'].nunique()}")
    print(f"  Male/Female: {df['Gender'].value_counts().to_dict()}")
    print(f"  Avg Salary:  ${df['MonthlyIncome'].mean():,.0f}")
    print(f"  Avg Age:     {df['Age'].mean():.1f} years")
    print(f"  Avg Tenure:  {df['YearsAtCompany'].mean():.1f} years")
    print(f"  Date Range:  {df['HireDate'].min()} to {df['HireDate'].max()}")

    # Save to CSV
    csv_path = os.path.join(OUTPUT_DIR, "hr_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] CSV: {csv_path}")

    # Save to Excel
    xlsx_path = os.path.join(OUTPUT_DIR, "hr_data.xlsx")
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
    print(f"[SAVED] Excel: {xlsx_path}")

    print("\n" + "=" * 60)
    print("  Dataset generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
