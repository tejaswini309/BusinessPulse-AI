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