# Data Dictionary (Version 1)

## Dataset: olist_customers_dataset.csv

| Column | Description |
|---------|-------------|
| customer_id | Unique customer identifier |
| customer_unique_id | Identifier for the same customer across multiple orders |
| customer_zip_code_prefix | Customer ZIP code prefix |
| customer_city | Customer city |
| customer_state | Customer state |

---

## Dataset: olist_orders_dataset.csv

| Column | Description |
|---------|-------------|
| order_id | Unique order identifier |
| customer_id | Customer who placed the order |
| order_status | Current order status |
| order_purchase_timestamp | Date and time of purchase |
| order_approved_at | Payment approval timestamp |
| order_delivered_carrier_date | Date handed to logistics partner |
| order_delivered_customer_date | Delivery completion date |
| order_estimated_delivery_date | Estimated delivery date |

---

## Dataset: olist_order_items_dataset.csv

| Column | Description |
|---------|-------------|
| order_id | Related order ID |
| order_item_id | Item number within the order |
| product_id | Purchased product |
| seller_id | Seller identifier |
| shipping_limit_date | Shipping deadline |
| price | Product price |
| freight_value | Shipping cost |

---

## Dataset: olist_order_payments_dataset.csv

| Column | Description |
|---------|-------------|
| order_id | Related order ID |
| payment_sequential | Payment sequence |
| payment_type | Payment method |
| payment_installments | Number of installments |
| payment_value | Total payment amount |

---

## Dataset: olist_products_dataset.csv

| Column | Description |
|---------|-------------|
| product_id | Product identifier |
| product_category_name | Product category |
| product_name_lenght | Product name length |
| product_description_lenght | Description length |
| product_photos_qty | Number of product images |
| product_weight_g | Product weight (grams) |
| product_length_cm | Product length |
| product_height_cm | Product height |
| product_width_cm | Product width |

---

## Dataset: product_category_name_translation.csv

| Column | Description |
|---------|-------------|
| product_category_name | Portuguese category name |
| product_category_name_english | English category name |