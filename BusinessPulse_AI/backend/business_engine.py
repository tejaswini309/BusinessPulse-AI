import pandas as pd
from data_loader import load_business_data


class BusinessEngine:

    def __init__(self):
        self.data = load_business_data()

        self.orders = self.data["orders"].copy()
        self.order_items = self.data["order_items"].copy()
        self.customers = self.data["customers"].copy()
        self.products = self.data["products"].copy()
        self.sellers = self.data["sellers"].copy()
        self.payments = self.data["payments"].copy()
        self.reviews = self.data["reviews"].copy()
        self.geolocation = self.data["geolocation"].copy()
        self.category_translation = self.data["category_translation"].copy()

        self._prepare_data()

    # ---------------------------------------------------------
    # DATA PREPARATION
    # ---------------------------------------------------------

    def _prepare_data(self):

        # Convert order dates
        date_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]

        for column in date_columns:
            if column in self.orders.columns:
                self.orders[column] = pd.to_datetime(
                    self.orders[column],
                    errors="coerce"
                )

        # Convert payment values
        self.payments["payment_value"] = pd.to_numeric(
            self.payments["payment_value"],
            errors="coerce"
        )

        # Convert order item financial values
        self.order_items["price"] = pd.to_numeric(
            self.order_items["price"],
            errors="coerce"
        )

        self.order_items["freight_value"] = pd.to_numeric(
            self.order_items["freight_value"],
            errors="coerce"
        )

        # Merge order items with orders
        self.order_items_orders = self.order_items.merge(
            self.orders[
                [
                    "order_id",
                    "customer_id",
                    "order_status",
                    "order_purchase_timestamp",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date"
                ]
            ],
            on="order_id",
            how="left"
        )

        # Add product category
        self.order_product_data = self.order_items_orders.merge(
            self.products[
                [
                    "product_id",
                    "product_category_name"
                ]
            ],
            on="product_id",
            how="left"
        )

        # Add English category names
        self.order_product_data = self.order_product_data.merge(
            self.category_translation,
            on="product_category_name",
            how="left"
        )

    # ---------------------------------------------------------
    # CORE BUSINESS KPIs
    # ---------------------------------------------------------

    def total_revenue(self):

        return float(
            self.order_items["price"].sum()
        )

    def total_orders(self):

        return int(
            self.orders["order_id"].nunique()
        )

    def total_customers(self):

        return int(
            self.customers["customer_unique_id"].nunique()
        )

    def total_sellers(self):

        return int(
            self.sellers["seller_id"].nunique()
        )

    def average_order_value(self):

        orders = self.total_orders()

        if orders == 0:
            return 0

        return self.total_revenue() / orders

    def total_freight_cost(self):

        return float(
            self.order_items["freight_value"].sum()
        )

    def total_payment_value(self):

        return float(
            self.payments["payment_value"].sum()
        )

    # ---------------------------------------------------------
    # ORDER PERFORMANCE
    # ---------------------------------------------------------

    def cancellation_rate(self):

        total = len(self.orders)

        if total == 0:
            return 0

        cancelled = (
            self.orders["order_status"]
            .eq("canceled")
            .sum()
        )

        return cancelled / total * 100

    def unavailable_orders(self):

        return int(
            self.orders["order_status"]
            .eq("unavailable")
            .sum()
        )

    # ---------------------------------------------------------
    # DELIVERY PERFORMANCE
    # ---------------------------------------------------------

    def late_delivery_rate(self):

        delivered = self.orders[
            self.orders["order_delivered_customer_date"].notna()
            &
            self.orders["order_estimated_delivery_date"].notna()
        ].copy()

        if len(delivered) == 0:
            return 0

        late = (
            delivered["order_delivered_customer_date"]
            >
            delivered["order_estimated_delivery_date"]
        ).sum()

        return late / len(delivered) * 100

    def average_delivery_days(self):

        delivered = self.orders[
            self.orders["order_purchase_timestamp"].notna()
            &
            self.orders["order_delivered_customer_date"].notna()
        ].copy()

        if len(delivered) == 0:
            return 0

        delivery_days = (
            delivered["order_delivered_customer_date"]
            -
            delivered["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400

        return float(delivery_days.mean())

    # ---------------------------------------------------------
    # CUSTOMER INSIGHTS
    # ---------------------------------------------------------

    def repeat_customer_rate(self):

        customer_orders = (
            self.orders
            .groupby("customer_id")
            .size()
        )

        if len(customer_orders) == 0:
            return 0

        repeat_customers = (
            customer_orders > 1
        ).sum()

        return repeat_customers / len(customer_orders) * 100

    # ---------------------------------------------------------
    # PRODUCT / CATEGORY ANALYSIS
    # ---------------------------------------------------------

    def top_categories(self, limit=10):

        result = (
            self.order_product_data
            .groupby("product_category_name_english")["price"]
            .sum()
            .sort_values(ascending=False)
            .head(limit)
        )

        return result.to_dict()

    def top_products(self, limit=10):

        result = (
            self.order_items
            .groupby("product_id")["price"]
            .sum()
            .sort_values(ascending=False)
            .head(limit)
        )

        return result.to_dict()

    # ---------------------------------------------------------
    # SELLER PERFORMANCE
    # ---------------------------------------------------------

    def top_sellers(self, limit=10):

        result = (
            self.order_items
            .groupby("seller_id")["price"]
            .sum()
            .sort_values(ascending=False)
            .head(limit)
        )

        return result.to_dict()

    # ---------------------------------------------------------
    # CUSTOMER SATISFACTION
    # ---------------------------------------------------------

    def average_review_score(self):

        return float(
            self.reviews["review_score"].mean()
        )

    # ---------------------------------------------------------
    # PAYMENT ANALYSIS
    # ---------------------------------------------------------

    def payment_distribution(self):

        result = (
            self.payments
            .groupby("payment_type")["payment_value"]
            .sum()
            .sort_values(ascending=False)
        )

        return result.to_dict()

    # ---------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------------------------------------

    def executive_summary(self):

        return {
            "total_revenue": round(
                self.total_revenue(), 2
            ),

            "total_orders": self.total_orders(),

            "total_customers": self.total_customers(),

            "total_sellers": self.total_sellers(),

            "average_order_value": round(
                self.average_order_value(), 2
            ),

            "total_freight_cost": round(
                self.total_freight_cost(), 2
            ),

            "total_payment_value": round(
                self.total_payment_value(), 2
            ),

            "cancellation_rate": round(
                self.cancellation_rate(), 2
            ),

            "unavailable_orders": self.unavailable_orders(),

            "late_delivery_rate": round(
                self.late_delivery_rate(), 2
            ),

            "average_delivery_days": round(
                self.average_delivery_days(), 2
            ),

            "repeat_customer_rate": round(
                self.repeat_customer_rate(), 2
            ),

            "average_review_score": round(
                self.average_review_score(), 2
            ),

            "top_categories": self.top_categories(),

            "top_products": self.top_products(),

            "top_sellers": self.top_sellers(),

            "payment_distribution": self.payment_distribution()
        }


# -------------------------------------------------------------
# TEST
# -------------------------------------------------------------

if __name__ == "__main__":

    engine = BusinessEngine()

    summary = engine.executive_summary()

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE AI - BUSINESS INTELLIGENCE ENGINE")
    print("=" * 70)

    for key, value in summary.items():

        print(f"\n{key}:")
        print(value)

    print("\n")
    print("=" * 70)
    print("BUSINESS ENGINE TEST COMPLETED")
    print("=" * 70)