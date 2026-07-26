# Dataset Relationship Mapping

## BusinessPulse AI Dataset Mapping

The BusinessPulse AI project uses multiple datasets that are connected through common business keys.

| Dataset | Primary Key | Connected To | Relationship |
|---------|-------------|--------------|--------------|
| Customers | customer_id | Orders | One customer can place multiple orders |
| Orders | order_id | Order Items | One order can contain multiple products |
| Orders | customer_id | Customers | Many orders belong to one customer |
| Order Items | product_id | Products | Each order item refers to one product |
| Order Items | seller_id | Sellers | Each product is sold by one seller |
| Order Payments | order_id | Orders | One order may contain multiple payments |
| Order Reviews | order_id | Orders | One review belongs to one order |
| Products | product_category_name | Category Translation | Used for English category names |

---

## Primary Business Entities

- Customers
- Orders
- Products
- Sellers
- Payments
- Reviews
- Categories

---

## Future Analysis

These relationships will be used for:

- Sales Analysis
- Customer Analysis
- Product Performance
- Seller Performance
- Payment Analysis
- Logistics Analysis
- Executive KPI Dashboard
