# Installation Guide

## HR Analytics Dashboard

---

## 1. Prerequisites

### Required Software
| Software | Version | Download Link |
|----------|---------|---------------|
| Python | 3.11+ | [python.org](https://python.org) |
| Git | Latest | [git-scm.com](https://git-scm.com) |
| PostgreSQL (optional) | 16+ | [postgresql.org](https://postgresql.org) |
| Power BI (optional) | Desktop | [powerbi.microsoft.com](https://powerbi.microsoft.com) |
| VS Code (optional) | Latest | [code.visualstudio.com](https://code.visualstudio.com) |

### System Requirements
- **OS**: Windows 10+, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 500 MB free space
- **Python**: Installed and added to PATH

---

## 2. Python Environment Setup

### 2.1 Verify Python Installation
```bash
python --version
# Expected: Python 3.11.x or higher

pip --version
# Expected: pip 23.x or higher
```

### 2.2 (Optional) Create Virtual Environment

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Clone & Setup

### 3.1 Clone Repository
```bash
git clone https://github.com/yourusername/HR-Analytics-Dashboard.git
cd HR-Analytics-Dashboard
```

### 3.2 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.3 Verify Installation
```bash
python -c "import pandas; import numpy; import matplotlib; import plotly; import openpyxl; print('All packages installed successfully')"
```

---

## 4. Quick Start

### 4.1 Generate Dataset
```bash
python data/generate_dataset.py
```

### 4.2 Clean Data
```bash
python python/clean_data.py
```

### 4.3 Validate Data
```bash
python python/validate_data.py
```

### 4.4 Run Analysis
```bash
python python/analysis.py
```

### 4.5 Generate Charts
```bash
python python/generate_charts.py
```

### 4.6 Export Reports
```bash
python python/export_reports.py
```

### 4.7 Launch Dashboard (Optional)
```bash
streamlit run python/dashboard.py
```

---

## 5. PostgreSQL Setup (Optional)

### 5.1 Install PostgreSQL
Download from [postgresql.org/download](https://www.postgresql.org/download/)

### 5.2 Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE hr_analytics;
\q
```

### 5.3 Run Schema
```bash
psql -U postgres -d hr_analytics -f sql/schema.sql
```

### 5.4 Import Data
```bash
# Option 1: Using psql (update path in insert.sql first)
psql -U postgres -d hr_analytics -f sql/insert.sql

# Option 2: Using Python
python -c "
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('data/cleaned/hr_data_cleaned.csv')
engine = create_engine('postgresql://postgres:password@localhost:5432/hr_analytics')
df.to_sql('fact_employee', engine, if_exists='replace', index=False)
print('Data imported successfully')
"
```

### 5.5 Run SQL Analysis
```bash
psql -U postgres -d hr_analytics -f sql/employee_analysis.sql
psql -U postgres -d hr_analytics -f sql/attrition_analysis.sql
psql -U postgres -d hr_analytics -f sql/salary_analysis.sql
psql -U postgres -d hr_analytics -f sql/promotion_analysis.sql
psql -U postgres -d hr_analytics -f sql/diversity_analysis.sql
psql -U postgres -d hr_analytics -f sql/overtime_analysis.sql
psql -U postgres -d hr_analytics -f sql/window_functions.sql
psql -U postgres -d hr_analytics -f sql/views.sql
psql -U postgres -d hr_analytics -f sql/stored_procedures.sql
```

---

## 6. Power BI Setup (Optional)

### 6.1 Install Power BI Desktop
Download from [powerbi.microsoft.com](https://powerbi.microsoft.com/desktop/)

### 6.2 Open Dashboard
1. Launch Power BI Desktop
2. Open `powerbi/HR_Analytics.pbix`
3. If prompted, update database connection settings
4. Review and publish as needed

### 6.3 Connect to Database
1. In Power BI, click "Get Data" → "PostgreSQL database"
2. Enter server: `localhost`, database: `hr_analytics`
3. Load tables: `fact_employee`, `dim_department`, `dim_job_role`
4. Create relationships between tables

---

## 7. Running the Full Pipeline

### 7.1 One-Command Execution

**Windows (Command Prompt):**
```bash
python data\generate_dataset.py && python python\clean_data.py && python python\validate_data.py && python python\analysis.py && python python\generate_charts.py && python python\export_reports.py
```

**macOS/Linux:**
```bash
python data/generate_dataset.py && python python/clean_data.py && python python/validate_data.py && python python/analysis.py && python python/generate_charts.py && python python/export_reports.py
```

### 7.2 Using Run Script (Optional)
Create a `run_pipeline.py` file:
```python
#!/usr/bin/env python3
"""Run the complete HR Analytics pipeline."""
import subprocess
import sys

scripts = [
    "data/generate_dataset.py",
    "python/clean_data.py",
    "python/validate_data.py",
    "python/analysis.py",
    "python/generate_charts.py",
    "python/export_reports.py"
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"  Running: {script}")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {script} failed:")
        print(result.stderr)
        sys.exit(1)

print("\n✅ Pipeline completed successfully!")
```

---

## 8. Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **pip install fails** | Upgrade pip: `pip install --upgrade pip` |
| **ModuleNotFoundError** | Install missing package: `pip install <package>` |
| **UnicodeEncodeError** | Set console encoding: `chcp 65001` (Windows) or `PYTHONIOENCODING=utf-8` |
| **FileNotFoundError** | Run from project root directory |
| **Permission denied** | Use `sudo` (Linux/macOS) or run as admin (Windows) |
| **Port already in use** | Change port in Streamlit or database config |

### 8.1 Windows-Specific Issues

**Issue**: Unicode characters not displaying in console
```bash
# Set console to UTF-8
chcp 65001
# Or set environment variable
set PYTHONIOENCODING=utf-8
```

**Issue**: Long path names
```bash
# Enable long paths in Windows 10/11
# Run PowerShell as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### 8.2 Python Environment Issues

**Issue**: Conflicting package versions
```bash
# Create fresh virtual environment
python -m venv fresh_venv
# Activate and reinstall
source fresh_venv/bin/activate  # Linux/macOS
fresh_venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 9. Verification Checklist

After installation, verify each component:

- [ ] Dataset generated: `data/raw/hr_data.csv` exists
- [ ] Data cleaned: `data/cleaned/hr_data_cleaned.csv` exists
- [ ] Validation passed: validation report generated
- [ ] Analysis complete: CSV files in `data/processed/`
- [ ] Charts generated: PNG files in `reports/screenshots/`
- [ ] HTML dashboard: File in `reports/html/`
- [ ] Excel report: File in `reports/excel/`
- [ ] Streamlit dashboard: Launches without errors
- [ ] PostgreSQL (optional): Tables created and data loaded
- [ ] Power BI (optional): Dashboard opens and connects

---

## 10. Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project
cd ..
rm -rf HR-Analytics-Dashboard  # Linux/macOS
rmdir /s HR-Analytics-Dashboard  # Windows

# Remove Python packages (if desired)
pip uninstall -r requirements.txt -y
```
