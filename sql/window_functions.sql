-- =====================================================
-- BusinessPulse AI
-- File: window_functions.sql
-- Purpose:
-- SQL Window Functions
-- =====================================================

USE businesspulse_ai;

-- =====================================================
-- WINDOW FUNCTION 1
-- Rank Products by Width
-- =====================================================

SELECT
    product_id,
    product_category_name,
    product_width_cm,
    RANK() OVER (ORDER BY product_width_cm DESC) AS width_rank
FROM products;


-- =====================================================
-- WINDOW FUNCTION 2
-- Running Total of Product Prices by Shipping Date
-- =====================================================

SELECT
    oi.order_id,
    oi.shipping_limit_date,
    oi.price,
    SUM(oi.price) OVER (
        ORDER BY oi.shipping_limit_date
    ) AS running_total_price
FROM order_items oi;

-- =====================================================
-- WINDOW FUNCTION 3
-- Compare Current Price with Previous Price
-- =====================================================

SELECT
    order_id,
    shipping_limit_date,
    price,
    LAG(price, 1) OVER (
        ORDER BY shipping_limit_date
    ) AS previous_price
FROM order_items;

-- =====================================================
-- WINDOW FUNCTION 4
-- Compare Current Price with Next Price
-- =====================================================

SELECT
    order_id,
    shipping_limit_date,
    price,
    LEAD(price, 1) OVER (
        ORDER BY shipping_limit_date
    ) AS next_price
FROM order_items;