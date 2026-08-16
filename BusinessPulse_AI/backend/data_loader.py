from pathlib import Path
import pandas as pd


# Main BusinessPulse-AI project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Location of your existing cleaned datasets
DATA_DIR = BASE_DIR / "data" / "processed"


def load_business_data():
    files = {
        "orders": "orders_clean.csv",
        "order_items": "order_items_clean.csv",
        "customers": "customers_clean.csv",
        "products": "products_clean.csv",
        "sellers": "sellers_clean.csv",
        "payments": "payments_clean.csv",
        "reviews": "reviews_clean.csv",
        "geolocation": "geolocation_clean.csv",
        "category_translation": "category_translation_clean.csv",
    }

    data = {}

    for name, filename in files.items():
        file_path = DATA_DIR / filename

        if file_path.exists():
            df = pd.read_csv(file_path)
            data[name] = df
            print(f"✓ Loaded {name}: {df.shape}")
        else:
            print(f"⚠ File not found: {file_path}")

    return data


if __name__ == "__main__":
    business_data = load_business_data()

    print("\n" + "=" * 50)
    print("BusinessPulse AI data loading complete")
    print("=" * 50)
    print(f"Tables loaded: {len(business_data)}")