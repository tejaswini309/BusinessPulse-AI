-- =====================================================
-- BusinessPulse AI
-- File: constraints.sql
-- Purpose:
-- Database Constraints and Data Integrity Rules
-- =====================================================

USE businesspulse_ai;

-- =====================================================
-- PRIMARY KEYS
-- =====================================================

-- Customers Table
ALTER TABLE customers
ADD PRIMARY KEY (customer_id);

-- Products Table
ALTER TABLE products
ADD PRIMARY KEY (product_id);

-- =====================================================
-- FUTURE FOREIGN KEYS
-- (To be added when complete Olist dataset is integrated)
-- =====================================================

-- Example:
--
-- ALTER TABLE order_items
-- ADD CONSTRAINT fk_product
-- FOREIGN KEY (product_id)
-- REFERENCES products(product_id);

--
-- ALTER TABLE orders
-- ADD CONSTRAINT fk_customer
-- FOREIGN KEY (customer_id)
-- REFERENCES customers(customer_id);

-- =====================================================
-- Notes
-- =====================================================
-- Primary Keys implemented:
-- ✔ customers.customer_id
-- ✔ products.product_id
--
-- Foreign Keys will be implemented after all related
-- tables are integrated into the database.