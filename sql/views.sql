-- =====================================================
-- BusinessPulse AI
-- File: views.sql
-- Purpose:
-- Reusable SQL Views for Business Reporting
-- =====================================================

USE businesspulse_ai;

-- =====================================================
-- VIEW 1
-- Customer Order Summary
-- =====================================================

CREATE OR REPLACE VIEW customer_order_summary AS
SELECT
    c.customer_id,
    c.customer_city,
    c.customer_state,
    o.order_id,
    o.order_status,
    op.payment_type,
    op.payment_value
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_payments op
    ON o.order_id = op.order_id;


    -- =====================================================
-- VIEW 2
-- State Sales Summary
-- =====================================================

CREATE OR REPLACE VIEW state_sales_summary AS
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(op.payment_value), 2) AS total_revenue,
    ROUND(AVG(op.payment_value), 2) AS average_order_value
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_payments op
    ON o.order_id = op.order_id
GROUP BY c.customer_state;