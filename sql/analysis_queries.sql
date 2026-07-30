-- =====================================================
-- QUERY 1
-- Customer Orders with Payment Information
-- =====================================================

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
-- QUERY 2
-- Product Sales Details
-- =====================================================

SELECT
    o.order_id,
    o.order_status,
    oi.order_item_id,
    p.product_category_name,
    p.product_photos_qty,
    oi.price,
    oi.freight_value
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON oi.product_id = p.product_id;


    -- =====================================================
-- QUERY 3
-- Total Payment by Customer City
-- =====================================================

SELECT
    c.customer_city,
    SUM(op.payment_value) AS total_payment
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_payments op
    ON o.order_id = op.order_id
GROUP BY c.customer_city
ORDER BY total_payment DESC;

-- =====================================================
-- QUERY 4
-- Total Payment by Customer State
-- =====================================================

SELECT
    c.customer_state,
    SUM(op.payment_value) AS total_payment
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_payments op
    ON o.order_id = op.order_id
GROUP BY c.customer_state
ORDER BY total_payment DESC;

-- =====================================================
-- QUERY 5
-- Total Payment by Payment Type
-- =====================================================

SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    SUM(payment_value) AS total_payment,
    AVG(payment_value) AS average_payment
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment DESC;

-- =====================================================
-- QUERY 6
-- Average Product Photos by Product Category
-- =====================================================

SELECT
    product_category_name,
    COUNT(*) AS total_products,
    AVG(product_photos_qty) AS avg_product_photos
FROM products
GROUP BY product_category_name
ORDER BY avg_product_photos DESC;

-- =====================================================
-- QUERY 7
-- Average Product Price by Customer State
-- =====================================================

SELECT
    c.customer_state,
    COUNT(oi.order_id) AS total_order_items,
    ROUND(AVG(oi.price), 2) AS avg_product_price,
    ROUND(SUM(oi.price), 2) AS total_sales
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_sales DESC;

-- =====================================================
-- QUERY 8
-- Product Category Sales Performance
-- =====================================================

SELECT
    p.product_category_name,
    COUNT(oi.order_item_id) AS products_sold,
    ROUND(AVG(oi.price), 2) AS average_price,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM products p
INNER JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC;