import json
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# BUSINESSPULSE AI - FORECASTING ENGINE
# ============================================================

class ForecastingEngine:
    """
    BusinessPulse AI Forecasting Engine

    Generates business forecasts from historical order data.

    Forecasts:
        1. Revenue
        2. Orders

    Uses the cleaned BusinessPulse datasets.
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        # ----------------------------------------------------
        # LOCATE PROJECT DATA DIRECTORY
        # ----------------------------------------------------

        # forecasting_engine.py is inside:
        #
        # BusinessPulse-AI/
        #     BusinessPulse_AI/
        #         backend/
        #             forecasting_engine.py
        #
        # The data directory is:
        #
        # BusinessPulse-AI/
        #     data/
        #         processed/
        #
        # Therefore we go two levels up from backend.

        BASE_DIR = (
            Path(__file__).resolve().parents[2]
        )

        DATA_DIR = (
            BASE_DIR / "data" / "processed"
        )


        # ----------------------------------------------------
        # DATA FILES
        # ----------------------------------------------------

        self.orders_file = (
            DATA_DIR / "orders_clean.csv"
        )

        self.order_items_file = (
            DATA_DIR / "order_items_clean.csv"
        )


        # ----------------------------------------------------
        # DISPLAY DATA PATH
        # ----------------------------------------------------

        print("\nForecasting data directory:")
        print(DATA_DIR)

        print("\nOrders file:")
        print(self.orders_file)

        print("\nOrder items file:")
        print(self.order_items_file)


        # ----------------------------------------------------
        # VALIDATE FILES
        # ----------------------------------------------------

        if not self.orders_file.exists():

            raise FileNotFoundError(
                "\nOrders dataset not found.\n"
                "Expected location:\n"
                f"{self.orders_file}"
            )


        if not self.order_items_file.exists():

            raise FileNotFoundError(
                "\nOrder items dataset not found.\n"
                "Expected location:\n"
                f"{self.order_items_file}"
            )


        print("\n✓ Forecasting datasets found.")


        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

        self.orders = pd.read_csv(
            self.orders_file
        )

        self.order_items = pd.read_csv(
            self.order_items_file
        )


        print(
            f"✓ Orders loaded: "
            f"{self.orders.shape}"
        )

        print(
            f"✓ Order items loaded: "
            f"{self.order_items.shape}"
        )


        # ----------------------------------------------------
        # REQUIRED COLUMNS
        # ----------------------------------------------------

        required_order_columns = [
            "order_id",
            "order_purchase_timestamp"
        ]

        required_item_columns = [
            "order_id",
            "price"
        ]


        # ----------------------------------------------------
        # CHECK ORDER COLUMNS
        # ----------------------------------------------------

        missing_order_columns = [
            column
            for column in required_order_columns
            if column not in self.orders.columns
        ]


        # ----------------------------------------------------
        # CHECK ORDER ITEM COLUMNS
        # ----------------------------------------------------

        missing_item_columns = [
            column
            for column in required_item_columns
            if column not in self.order_items.columns
        ]


        if missing_order_columns:

            raise ValueError(
                "\nMissing required columns "
                "in orders_clean.csv:\n"
                f"{missing_order_columns}\n\n"
                "Available columns:\n"
                f"{list(self.orders.columns)}"
            )


        if missing_item_columns:

            raise ValueError(
                "\nMissing required columns "
                "in order_items_clean.csv:\n"
                f"{missing_item_columns}\n\n"
                "Available columns:\n"
                f"{list(self.order_items.columns)}"
            )


        print(
            "✓ Required columns validated."
        )


        # ----------------------------------------------------
        # CONVERT ORDER DATE
        # ----------------------------------------------------

        self.orders[
            "order_purchase_timestamp"
        ] = pd.to_datetime(
            self.orders[
                "order_purchase_timestamp"
            ],
            errors="coerce"
        )


        # ----------------------------------------------------
        # REMOVE INVALID DATES
        # ----------------------------------------------------

        before_rows = len(
            self.orders
        )

        self.orders = self.orders.dropna(
            subset=[
                "order_purchase_timestamp"
            ]
        )

        after_rows = len(
            self.orders
        )


        print(
            f"✓ Valid order dates: "
            f"{after_rows}"
        )


        if before_rows != after_rows:

            print(
                f"✓ Removed invalid dates: "
                f"{before_rows - after_rows}"
            )


        # ----------------------------------------------------
        # MERGE ORDER ITEMS WITH ORDERS
        # ----------------------------------------------------

        self.data = self.order_items.merge(
            self.orders[
                [
                    "order_id",
                    "order_purchase_timestamp"
                ]
            ],
            on="order_id",
            how="inner"
        )


        print(
            "✓ Forecasting dataset prepared: "
            f"{self.data.shape}"
        )


        # ----------------------------------------------------
        # INITIALIZATION COMPLETE
        # ----------------------------------------------------

        print(
            "\n✓ Forecasting engine initialized."
        )


    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

    def monthly_revenue(self):

        monthly = (
            self.data
            .set_index(
                "order_purchase_timestamp"
            )
            .resample("ME")["price"]
            .sum()
            .reset_index()
        )


        monthly.columns = [
            "month",
            "revenue"
        ]


        return monthly


    # ========================================================
    # MONTHLY ORDERS
    # ========================================================

    def monthly_orders(self):

        monthly = (
            self.orders
            .set_index(
                "order_purchase_timestamp"
            )
            .resample("ME")["order_id"]
            .nunique()
            .reset_index()
        )


        monthly.columns = [
            "month",
            "orders"
        ]


        return monthly


    # ========================================================
    # LINEAR TREND FORECAST
    # ========================================================

    def _linear_forecast(
        self,
        values,
        periods=3
    ):
        """
        Generate future values using a simple
        linear trend.

        This first forecasting version is designed
        to be transparent and explainable.
        """

        values = np.asarray(
            values,
            dtype=float
        )


        # ----------------------------------------------------
        # MINIMUM DATA CHECK
        # ----------------------------------------------------

        if len(values) < 3:

            return []


        # ----------------------------------------------------
        # HISTORICAL INDEX
        # ----------------------------------------------------

        x = np.arange(
            len(values)
        )


        # ----------------------------------------------------
        # FIT LINEAR TREND
        # ----------------------------------------------------

        slope, intercept = np.polyfit(
            x,
            values,
            1
        )


        # ----------------------------------------------------
        # FUTURE INDEX
        # ----------------------------------------------------

        future_x = np.arange(
            len(values),
            len(values) + periods
        )


        # ----------------------------------------------------
        # PREDICTIONS
        # ----------------------------------------------------

        predictions = (
            slope * future_x
            + intercept
        )


        # ----------------------------------------------------
        # PREVENT NEGATIVE VALUES
        # ----------------------------------------------------

        predictions = np.maximum(
            predictions,
            0
        )


        return predictions.tolist()


    # ========================================================
    # REVENUE FORECAST
    # ========================================================

    def forecast_revenue(
        self,
        periods=3
    ):

        monthly = (
            self.monthly_revenue()
        )


        # ----------------------------------------------------
        # DATA SUFFICIENCY CHECK
        # ----------------------------------------------------

        if len(monthly) < 3:

            return {

                "status":
                    "insufficient_data",

                "message":
                    "Not enough monthly revenue "
                    "history to generate a forecast."

            }


        # ----------------------------------------------------
        # GENERATE PREDICTIONS
        # ----------------------------------------------------

        predictions = (
            self._linear_forecast(
                monthly["revenue"].values,
                periods
            )
        )


        # ----------------------------------------------------
        # LAST HISTORICAL MONTH
        # ----------------------------------------------------

        last_month = (
            monthly["month"].iloc[-1]
        )


        # ----------------------------------------------------
        # FUTURE MONTHS
        # ----------------------------------------------------

        future_dates = pd.date_range(
            start=(
                last_month
                + pd.offsets.MonthEnd(1)
            ),
            periods=periods,
            freq="ME"
        )


        # ----------------------------------------------------
        # BUILD FORECAST
        # ----------------------------------------------------

        forecast = []


        for date, value in zip(
            future_dates,
            predictions
        ):

            forecast.append({

                "month":
                    date.strftime("%Y-%m"),

                "forecast_revenue":
                    round(
                        float(value),
                        2
                    )

            })


        # ----------------------------------------------------
        # HISTORICAL VALUES
        # ----------------------------------------------------

        historical_values = (
            monthly["revenue"].values
        )


        # ----------------------------------------------------
        # DETERMINE TREND
        # ----------------------------------------------------

        if (
            historical_values[-1]
            >
            historical_values[-2]
        ):

            trend = "Increasing"


        elif (
            historical_values[-1]
            <
            historical_values[-2]
        ):

            trend = "Decreasing"


        else:

            trend = "Stable"


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "status":
                "success",

            "metric":
                "Revenue",

            "historical_months":
                len(monthly),

            "last_actual_month":
                last_month.strftime(
                    "%Y-%m"
                ),

            "last_actual_revenue":
                round(
                    float(
                        historical_values[-1]
                    ),
                    2
                ),

            "trend":
                trend,

            "forecast_periods":
                periods,

            "forecast":
                forecast
        }


    # ========================================================
    # ORDER FORECAST
    # ========================================================

    def forecast_orders(
        self,
        periods=3
    ):

        monthly = (
            self.monthly_orders()
        )


        # ----------------------------------------------------
        # DATA SUFFICIENCY CHECK
        # ----------------------------------------------------

        if len(monthly) < 3:

            return {

                "status":
                    "insufficient_data",

                "message":
                    "Not enough monthly order "
                    "history to generate a forecast."

            }


        # ----------------------------------------------------
        # GENERATE PREDICTIONS
        # ----------------------------------------------------

        predictions = (
            self._linear_forecast(
                monthly["orders"].values,
                periods
            )
        )


        # ----------------------------------------------------
        # LAST HISTORICAL MONTH
        # ----------------------------------------------------

        last_month = (
            monthly["month"].iloc[-1]
        )


        # ----------------------------------------------------
        # FUTURE MONTHS
        # ----------------------------------------------------

        future_dates = pd.date_range(
            start=(
                last_month
                + pd.offsets.MonthEnd(1)
            ),
            periods=periods,
            freq="ME"
        )


        # ----------------------------------------------------
        # BUILD FORECAST
        # ----------------------------------------------------

        forecast = []


        for date, value in zip(
            future_dates,
            predictions
        ):

            forecast.append({

                "month":
                    date.strftime("%Y-%m"),

                "forecast_orders":
                    round(
                        float(value),
                        0
                    )

            })


        # ----------------------------------------------------
        # HISTORICAL VALUES
        # ----------------------------------------------------

        historical_values = (
            monthly["orders"].values
        )


        # ----------------------------------------------------
        # DETERMINE TREND
        # ----------------------------------------------------

        if (
            historical_values[-1]
            >
            historical_values[-2]
        ):

            trend = "Increasing"


        elif (
            historical_values[-1]
            <
            historical_values[-2]
        ):

            trend = "Decreasing"


        else:

            trend = "Stable"


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "status":
                "success",

            "metric":
                "Orders",

            "historical_months":
                len(monthly),

            "last_actual_month":
                last_month.strftime(
                    "%Y-%m"
                ),

            "last_actual_orders":
                int(
                    historical_values[-1]
                ),

            "trend":
                trend,

            "forecast_periods":
                periods,

            "forecast":
                forecast
        }


    # ========================================================
    # COMPLETE FORECAST
    # ========================================================

    def generate_forecast(
        self,
        periods=3
    ):

        revenue_forecast = (
            self.forecast_revenue(
                periods
            )
        )


        order_forecast = (
            self.forecast_orders(
                periods
            )
        )


        return {

            "status":
                "success",

            "forecast_horizon_months":
                periods,

            "revenue_forecast":
                revenue_forecast,

            "order_forecast":
                order_forecast
        }


# ============================================================
# FORECASTING ENGINE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print(
        "BUSINESSPULSE AI - FORECASTING ENGINE TEST"
    )
    print("=" * 70)


    try:

        # ----------------------------------------------------
        # CREATE ENGINE
        # ----------------------------------------------------

        print(
            "\n[1/4] Loading forecasting engine..."
        )


        engine = ForecastingEngine()


        print(
            "✓ Forecasting engine loaded"
        )


        # ----------------------------------------------------
        # REVENUE FORECAST
        # ----------------------------------------------------

        print(
            "\n[2/4] Generating revenue forecast..."
        )


        revenue = (
            engine.forecast_revenue(
                periods=3
            )
        )


        print(
            "✓ Revenue forecast generated"
        )


        print(
            "\nRevenue Forecast:"
        )


        print(
            json.dumps(
                revenue,
                indent=4,
                ensure_ascii=False,
                default=str
            )
        )


        # ----------------------------------------------------
        # ORDER FORECAST
        # ----------------------------------------------------

        print(
            "\n[3/4] Generating order forecast..."
        )


        orders = (
            engine.forecast_orders(
                periods=3
            )
        )


        print(
            "✓ Order forecast generated"
        )


        print(
            "\nOrder Forecast:"
        )


        print(
            json.dumps(
                orders,
                indent=4,
                ensure_ascii=False,
                default=str
            )
        )


        # ----------------------------------------------------
        # COMPLETE FORECAST
        # ----------------------------------------------------

        print(
            "\n[4/4] Generating complete forecast..."
        )


        complete_forecast = (
            engine.generate_forecast(
                periods=3
            )
        )


        print(
            "✓ Complete forecast generated"
        )


        print(
            "\nComplete Forecast:"
        )


        print(
            json.dumps(
                complete_forecast,
                indent=4,
                ensure_ascii=False,
                default=str
            )
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print("\n")
        print("=" * 70)
        print(
            "FORECASTING ENGINE TEST COMPLETED"
        )
        print("=" * 70)


    except Exception as error:

        print("\n")
        print("=" * 70)
        print(
            "FORECASTING ENGINE ERROR"
        )
        print("=" * 70)


        print(
            f"\n{error}"
        )


        print("\nCheck:")

        print(
            "1. Data folder location"
        )

        print(
            "2. CSV filenames"
        )

        print(
            "3. Dataset columns"
        )

        print("=" * 70)