-- =====================================================
-- BusinessPulse AI
-- File: import_data.sql
-- Description:
-- This script documents the data import process for the
-- sample Olist datasets used in Day 8.
-- =====================================================

USE businesspulse_ai;

-- =====================================================
-- Imported Tables
-- =====================================================

-- customers
-- Source File:
-- olist_customers_dataset_sample.csv

-- Imported using:
-- MySQL Workbench → Table Data Import Wizard

-- -----------------------------------------------------

-- order_payments
-- Source File:
-- olist_order_payments_dataset_sample.csv

-- Imported using:
-- MySQL Workbench → Table Data Import Wizard

-- -----------------------------------------------------

-- products
-- Source File:
-- olist_products_dataset_sample.csv

-- Imported using:
-- MySQL Workbench → Table Data Import Wizard

-- -----------------------------------------------------

-- order_items
-- Source File:
-- olist_order_items_dataset_sample.csv

-- Imported using:
-- MySQL Workbench → Table Data Import Wizard

-- -----------------------------------------------------

-- geolocation
-- Source File:
-- olist_geolocation_dataset_sample.csv

-- Imported using:
-- MySQL Workbench → Table Data Import Wizard

-- =====================================================
-- Import Verification Queries
-- =====================================================

SELECT COUNT(*) AS customers_count FROM customers;

SELECT COUNT(*) AS payments_count FROM order_payments;

SELECT COUNT(*) AS products_count FROM products;

SELECT COUNT(*) AS order_items_count FROM order_items;

SELECT COUNT(*) AS geolocation_count FROM geolocation;
# SQL Module - BusinessPulse AI

## Overview

This folder contains all SQL scripts used for designing, validating, and managing the BusinessPulse AI database.

The SQL module is organized to follow professional database development practices by separating schema creation, data import, data cleaning, and database constraints into individual files.

---

## Folder Structure

```
sql/
├── schema.sql
├── import_data.sql
├── data_cleaning.sql
├── constraints.sql
└── README.md
```

---

## File Description

### schema.sql

Creates the BusinessPulse AI database and all required tables.

Tables Included:

- customers
- products
- order_items
- order_payments
- geolocation

---

### import_data.sql

Documents the data import process for the Olist sample datasets.

Includes:

- Source CSV files
- Import method
- Record verification queries

---

### data_cleaning.sql

Contains SQL queries used for validating data quality.

Checks performed:

- NULL value validation
- Duplicate record detection
- Table structure verification
- Record count validation

---

### constraints.sql

Documents database integrity constraints.

Includes:

- Primary Keys
- Future Foreign Key relationships
- Data integrity notes

---

## Database

Database Name

businesspulse_ai

---

## Tools Used

- MySQL Workbench
- SQL
- Olist Sample Dataset
- GitHub

---

## Project Status

Current Progress

- Database Schema ✔
- Data Import ✔
- Data Validation ✔
- Data Cleaning ✔
- Constraints Documentation ✔

---

Future Enhancements

- SQL Analysis Queries
- Views
- Stored Procedures
- Indexes
- Business KPIs