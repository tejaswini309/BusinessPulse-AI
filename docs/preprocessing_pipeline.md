# Data Preprocessing Pipeline

## Project

BusinessPulse AI – Enterprise Decision Intelligence Platform

---

# Pipeline Overview

The preprocessing pipeline ensures that raw business data is transformed into a clean, reliable, and analysis-ready dataset before performing SQL analytics, Power BI visualization, and machine learning.

---

## Phase 1 – Data Collection

- Imported all Olist e-commerce datasets.
- Verified dataset availability.
- Organized raw files under the `data/raw` directory.

**Output:**
- Raw datasets ready for validation.

---

## Phase 2 – Data Validation

Performed initial quality assessment:

- Checked dataset dimensions.
- Reviewed column names.
- Identified missing values.
- Detected duplicate records.
- Examined data types.
- Verified primary business identifiers.

**Output:**
- Data validation report.

---

## Phase 3 – Data Cleaning

Applied preprocessing techniques:

- Handled missing values using appropriate strategies.
- Filled product attributes using median values where applicable.
- Replaced missing review text with placeholder values.
- Standardized column formats.
- Converted timestamp columns to datetime format.
- Preserved valid business-related missing values (e.g., undelivered orders).

**Output:**
- Cleaned datasets stored in `data/processed`.

---

## Phase 4 – Data Integrity Validation

Verified preprocessing quality:

- Compared raw and cleaned row counts.
- Ensured no unintended data loss.
- Reviewed missing values after cleaning.
- Validated data types.
- Confirmed successful dataset loading.

**Output:**
- Data validation summary.

---

## Phase 5 – Analysis Ready

The processed datasets are now ready for:

- Exploratory Data Analysis (EDA)
- SQL analytics
- KPI calculation
- Power BI dashboard development
- Business insight generation
- Machine Learning (future enhancement)

---

# Folder Flow

data/raw
↓
Data Validation
↓
Data Cleaning
↓
data/processed
↓
EDA
↓
SQL Analytics
↓
Power BI Dashboard
↓
Business Insights