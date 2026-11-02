"""Chapter 3: pandas essentials, run on the sample orders in data/."""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"
OUTPUT = HERE / "output"
EUR_TO_MAD = 10.8  # example rate; use a real rate source in production

df = pd.read_csv(DATA / "orders.csv", parse_dates=["ordered_at"])

# 1. Always look before you transform
print(df.head(), "\n")
df.info()
print("\n", df.describe(), "\n")

# 2. Select and filter
paid = df[df["status"] == "paid"]
small = df[["order_id", "city", "amount_eur"]]
print(f"{len(paid)} paid orders out of {len(df)}")

# 3. Create new columns
df["amount_mad"] = (df["amount_eur"] * EUR_TO_MAD).round(2)
df["order_month"] = df["ordered_at"].dt.to_period("M").astype(str)

# 4. Clean
df = df.drop_duplicates(subset="order_id")
df["city"] = df["city"].str.strip().str.title()
df = df.dropna(subset=["amount_mad"])
df = df[df["amount_mad"] >= 0]          # a negative amount is impossible here

# 5. Aggregate
monthly = (
    df[df["status"] == "paid"]
    .groupby(["order_month", "city"], as_index=False)
    .agg(revenue_mad=("amount_mad", "sum"), orders=("order_id", "count"))
    .sort_values(["order_month", "revenue_mad"], ascending=[True, False])
)
print("\nMonthly revenue by city:\n", monthly.to_string(index=False))

# 6. Join with customers
customers = pd.read_csv(DATA / "customers.csv")
enriched = df.merge(customers, on="customer_id", how="left")
print("\nRevenue by segment (MAD):\n", enriched.groupby("segment")["amount_mad"].sum().round(2))

# 7. Save
OUTPUT.mkdir(exist_ok=True)
try:
    monthly.to_parquet(OUTPUT / "monthly_revenue.parquet", index=False)
    print(f"\nSaved {OUTPUT / 'monthly_revenue.parquet'}")
except ImportError:
    monthly.to_csv(OUTPUT / "monthly_revenue.csv", index=False)
    print("\npyarrow is not installed, so the result was saved as CSV instead of Parquet.")
