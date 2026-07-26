# Data Cleaning Strategy

## Objectives

Ensure high-quality, analysis-ready datasets while preserving business meaning.

## Principles

- Preserve raw datasets.
- Clean only working copies.
- Document every transformation.
- Maintain reproducibility.

## Missing Values

- Business-valid missing values are retained where appropriate.
- Product numeric attributes are imputed using the median.
- Missing review text is replaced with descriptive placeholders.

## Data Types

- Date columns are converted to datetime format.

## Duplicates

- Business-valid duplicates (e.g., geolocation) are retained.

## Output

All cleaned datasets will be stored in the `data/processed/` directory.
