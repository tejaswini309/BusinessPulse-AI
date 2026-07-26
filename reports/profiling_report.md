# Data Profiling Report

## Overview

Data profiling was performed to evaluate the quality of the raw Olist datasets before data cleaning and preprocessing.

## Data Type Validation

- Reviewed data types across all datasets.
- Identified date columns stored as text in the raw dataset.
- Verified numeric columns for prices, payment values, and product dimensions.

## Missing Values

- Missing values were found primarily in delivery dates, review comments, and some product attributes.
- These missing values are consistent with the original dataset and require business-aware handling.

## Duplicate Analysis

- No duplicate records were found in the primary business datasets.
- The geolocation dataset contains expected duplicate ZIP code prefixes.

## Invalid Value Checks

- Checked price, payment values, and product photo quantities for invalid or out-of-range values.
- No critical data quality issues requiring immediate removal were identified.

## Category Consistency

- Reviewed customer states, customer cities, and payment types.
- No major category inconsistencies affecting analysis were identified.

## Conclusion

The raw datasets passed the initial profiling stage and are ready for the data cleaning and preprocessing phase.

