from data_loader import load_business_data


data = load_business_data()

output = []

output.append("=" * 70)
output.append("BUSINESSPULSE AI - DATA SCHEMA")
output.append("=" * 70)

for name, df in data.items():

    output.append("")
    output.append("=" * 70)
    output.append(f"TABLE: {name.upper()}")
    output.append(f"ROWS: {len(df):,}")
    output.append(f"COLUMNS: {len(df.columns)}")
    output.append("-" * 70)

    for column in df.columns:
        output.append(f"{column} | {df[column].dtype}")

report = "\n".join(output)

print(report)

with open("data_schema.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("\n✓ Schema saved to data_schema.txt")