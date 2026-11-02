"""Chapter 8: generate fake orders for the big-data exercises.

usage: python make_orders.py [--rows 5000000]
Writes data/orders.csv and, when pyarrow is installed, data/orders.parquet.
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--rows", type=int, default=5_000_000)
args = parser.parse_args()

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
n = args.rows
cities = np.array(["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier",
                   "Agadir", "Meknes", "Oujda", "Kenitra", "Tetouan"])
start = np.datetime64("2024-01-01T00:00")

t0 = time.perf_counter()
df = pd.DataFrame({
    "order_id": np.arange(1, n + 1),
    "customer_id": rng.integers(1, 200_001, n),
    "city": cities[rng.integers(0, len(cities), n)],
    "amount": rng.gamma(2.0, 120.0, n).round(2),
    "status": rng.choice(["paid", "refunded", "cancelled"], n, p=[0.90, 0.06, 0.04]),
    "ordered_at": start + rng.integers(0, 2 * 365 * 24 * 60, n).astype("timedelta64[m]"),
})
print(f"Generated {n:,} orders in {time.perf_counter() - t0:.1f} s")

df.to_csv(DATA / "orders.csv", index=False)
print(f"CSV:     {(DATA / 'orders.csv').stat().st_size / 1e6:8.1f} MB")
try:
    df.to_parquet(DATA / "orders.parquet", index=False)
    print(f"Parquet: {(DATA / 'orders.parquet').stat().st_size / 1e6:8.1f} MB")
except ImportError:
    print("Install pyarrow to also write the Parquet file: pip install pyarrow")
