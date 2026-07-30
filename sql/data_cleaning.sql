-- =====================================================
-- BusinessPulse AI
-- File: data_cleaning.sql
-- Purpose:
-- Data Quality Validation and Cleaning Queries
-- =====================================================

USE businesspulse_ai;

-- =====================================================
-- 1. NULL VALUE CHECK
-- =====================================================

SELECT
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(customer_unique_id IS NULL) AS customer_unique_id_nulls,
    SUM(customer_zip_code_prefix IS NULL) AS zip_code_nulls,
    SUM(customer_city IS NULL) AS city_nulls,
    SUM(customer_state IS NULL) AS state_nulls
FROM customers;

-- =====================================================
-- 2. DUPLICATE CHECK
-- =====================================================

SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- =====================================================
-- 3. TABLE STRUCTURE VALIDATION
-- =====================================================

DESCRIBE customers;

DESCRIBE products;

DESCRIBE order_items;

DESCRIBE order_payments;

DESCRIBE geolocation;

-- =====================================================
-- 4. RECORD COUNT VALIDATION
-- =====================================================

SELECT COUNT(*) AS customers FROM customers;

SELECT COUNT(*) AS products FROM products;

SELECT COUNT(*) AS order_items FROM order_items;

SELECT COUNT(*) AS payments FROM order_payments;

SELECT COUNT(*) AS geolocations FROM geolocation;

-- =====================================================
-- Notes
-- =====================================================
-- ✔ NULL values checked
-- ✔ Duplicate records checked
-- ✔ Table structures verified
-- ✔ Record counts validated
