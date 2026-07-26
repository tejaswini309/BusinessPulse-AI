# Cleaning Decision Matrix

## Project

BusinessPulse AI – Enterprise Decision Intelligence Platform

---

| Dataset | Column | Issue | Decision | Reason |
|---------|--------|-------|----------|--------|
| Orders | order_approved_at | Missing Values | Keep | Orders may still be pending approval. Missing values are business-valid. |
| Orders | order_delivered_carrier_date | Missing Values | Keep | Orders not yet shipped will not have a carrier date. |
| Orders | order_delivered_customer_date | Missing Values | Keep | Undelivered or canceled orders naturally have missing delivery dates. |
| Reviews | review_comment_title | Missing Values | Keep | Customers are not required to provide review titles. |
| Reviews | review_comment_message | Missing Values | Keep | Many customers rate products without writing comments. |
| Products | product_name_lenght | Missing Values | Impute | Missing numeric metadata can be filled using the median. |
| Products | product_description_lenght | Missing Values | Impute | Median is suitable for missing description lengths. |
| Products | product_photos_qty | Missing Values | Impute | Missing values can be replaced using the median. |
| Products | product_weight_g | Missing Values | Impute | Replace missing values with the median to preserve distribution. |
| Products | product_length_cm | Missing Values | Impute | Median is robust against outliers. |
| Products | product_height_cm | Missing Values | Impute | Median is appropriate for physical dimensions. |
| Products | product_width_cm | Missing Values | Impute | Median is appropriate for physical dimensions. |
| Geolocation | Duplicate Rows | Duplicate Records | Keep | Duplicate ZIP code prefixes are expected in the original dataset and represent valid locations. |
| Orders | Date Columns | Incorrect Data Type | Convert | Convert from object to datetime for analysis. |
