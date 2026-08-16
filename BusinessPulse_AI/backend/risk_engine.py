from business_engine import BusinessEngine
import pandas as pd


class RiskEngine:

    def __init__(self):

        self.engine = BusinessEngine()

        self.orders = self.engine.orders
        self.order_items = self.engine.order_items

    # ---------------------------------------------------------
    # RISK 1 — LATE DELIVERY
    # ---------------------------------------------------------

    def late_delivery_risk(self):

        rate = self.engine.late_delivery_rate()

        if rate >= 10:
            level = "HIGH"
            message = (
                f"Late delivery rate is {rate:.2f}%, "
                "which is above the 10% target."
            )

        elif rate >= 7:
            level = "MEDIUM"
            message = (
                f"Late delivery rate is {rate:.2f}%. "
                "Delivery performance requires monitoring."
            )

        else:
            level = "LOW"
            message = (
                f"Late delivery rate is {rate:.2f}%. "
                "Delivery performance is currently healthy."
            )

        return {
            "risk": "Late Delivery",
            "level": level,
            "value": round(rate, 2),
            "message": message
        }

    # ---------------------------------------------------------
    # RISK 2 — CANCELLATION
    # ---------------------------------------------------------

    def cancellation_risk(self):

        rate = self.engine.cancellation_rate()

        if rate >= 2:
            level = "HIGH"

        elif rate >= 1:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk": "Cancellation",
            "level": level,
            "value": round(rate, 2),
            "message": (
                f"Cancellation rate is {rate:.2f}%."
            )
        }

    # ---------------------------------------------------------
    # RISK 3 — CUSTOMER SATISFACTION
    # ---------------------------------------------------------

    def satisfaction_risk(self):

        score = self.engine.average_review_score()

        if score < 3.5:
            level = "HIGH"

        elif score < 4:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk": "Customer Satisfaction",
            "level": level,
            "value": round(score, 2),
            "message": (
                f"Average review score is {score:.2f}/5."
            )
        }

    # ---------------------------------------------------------
    # RISK 4 — FREIGHT COST
    # ---------------------------------------------------------

    def freight_cost_risk(self):

        revenue = self.engine.total_revenue()
        freight = self.engine.total_freight_cost()

        if revenue == 0:
            ratio = 0
        else:
            ratio = (freight / revenue) * 100

        if ratio >= 20:
            level = "HIGH"

        elif ratio >= 15:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk": "Freight Cost",
            "level": level,
            "value": round(ratio, 2),
            "message": (
                f"Freight cost represents {ratio:.2f}% "
                "of product revenue."
            )
        }

    # ---------------------------------------------------------
    # RISK 5 — REVENUE CONCENTRATION
    # ---------------------------------------------------------

    def revenue_concentration_risk(self):

        categories = self.engine.top_categories(limit=5)

        total_revenue = self.engine.total_revenue()

        top_revenue = sum(categories.values())

        if total_revenue == 0:
            concentration = 0
        else:
            concentration = (
                top_revenue / total_revenue
            ) * 100

        if concentration >= 60:
            level = "HIGH"

        elif concentration >= 45:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk": "Revenue Concentration",
            "level": level,
            "value": round(concentration, 2),
            "message": (
                f"Top 5 product categories contribute "
                f"{concentration:.2f}% of revenue."
            )
        }

    # ---------------------------------------------------------
    # ANOMALY — MONTHLY REVENUE
    # ---------------------------------------------------------

    def revenue_anomaly(self):

        data = self.order_items.copy()

        orders = self.orders[
            [
                "order_id",
                "order_purchase_timestamp"
            ]
        ].copy()

        orders["order_purchase_timestamp"] = pd.to_datetime(
            orders["order_purchase_timestamp"],
            errors="coerce"
        )

        data = data.merge(
            orders,
            on="order_id",
            how="left"
        )

        data = data.dropna(
            subset=["order_purchase_timestamp"]
        )

        data["year_month"] = (
            data["order_purchase_timestamp"]
            .dt.to_period("M")
        )

        monthly_revenue = (
            data.groupby("year_month")["price"]
            .sum()
            .sort_index()
        )

        if len(monthly_revenue) < 2:

            return {
                "risk": "Revenue Anomaly",
                "level": "LOW",
                "value": 0,
                "message": "Not enough historical data."
            }

        latest = monthly_revenue.iloc[-1]
        previous = monthly_revenue.iloc[-2]

        if previous == 0:
            change = 0
        else:
            change = (
                (latest - previous)
                / previous
            ) * 100

        if change <= -20:
            level = "HIGH"

        elif change <= -10:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk": "Revenue Anomaly",
            "level": level,
            "value": round(change, 2),
            "message": (
                f"Latest monthly revenue changed by "
                f"{change:.2f}% compared with the previous month."
            )
        }

    # ---------------------------------------------------------
    # RUN ALL RISK CHECKS
    # ---------------------------------------------------------

    def analyze_risks(self):

        risks = [

            self.late_delivery_risk(),

            self.cancellation_risk(),

            self.satisfaction_risk(),

            self.freight_cost_risk(),

            self.revenue_concentration_risk(),

            self.revenue_anomaly()

        ]

        high = [
            risk for risk in risks
            if risk["level"] == "HIGH"
        ]

        medium = [
            risk for risk in risks
            if risk["level"] == "MEDIUM"
        ]

        low = [
            risk for risk in risks
            if risk["level"] == "LOW"
        ]

        return {
            "all_risks": risks,
            "high_risks": high,
            "medium_risks": medium,
            "low_risks": low,
            "total_risks": len(risks),
            "high_count": len(high),
            "medium_count": len(medium),
            "low_count": len(low)
        }


# -------------------------------------------------------------
# TEST
# -------------------------------------------------------------

if __name__ == "__main__":

    risk_engine = RiskEngine()

    results = risk_engine.analyze_risks()

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE AI - RISK & ANOMALY ENGINE")
    print("=" * 70)

    print(
        f"\nTotal risks analyzed: "
        f"{results['total_risks']}"
    )

    print(
        f"High risks: "
        f"{results['high_count']}"
    )

    print(
        f"Medium risks: "
        f"{results['medium_count']}"
    )

    print(
        f"Low risks: "
        f"{results['low_count']}"
    )

    print("\n")
    print("-" * 70)
    print("RISK DETAILS")
    print("-" * 70)

    for risk in results["all_risks"]:

        print(
            f"\n[{risk['level']}] "
            f"{risk['risk']}"
        )

        print(
            f"Value: {risk['value']}"
        )

        print(
            f"Message: {risk['message']}"
        )

    print("\n")
    print("=" * 70)
    print("RISK ENGINE TEST COMPLETED")
    print("=" * 70)