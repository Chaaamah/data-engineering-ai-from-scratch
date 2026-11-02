"""Exercise 8.2: partition the orders by month and query a single month.

Needs pyarrow and duckdb. Run ../make_orders.py first.
"""
import time
from pathlib import Path

import duckdb
import pandas as pd

DATA = Path(__file__).parents[1] / "data"
target = DATA / "orders_by_month"

df = pd.read_parquet(DATA / "orders.parquet")
df["order_month"] = df["ordered_at"].dt.strftime("%Y-%m")
df.to_parquet(target, partition_cols=["order_month"], index=False)
print(f"Wrote {df['order_month'].nunique()} monthly folders under {target}")


def timed(label, sql):
    t0 = time.perf_counter()
    value = duckdb.sql(sql).fetchone()[0]
    print(f"{label:<44} {time.perf_counter() - t0:6.3f} s   revenue = {value:,.2f}")


timed("one month, single file (full scan)", f"""
    SELECT SUM(amount) FROM '{DATA / 'orders.parquet'}'
    WHERE status = 'paid'
      AND ordered_at >= TIMESTAMP '2025-06-01' AND ordered_at < TIMESTAMP '2025-07-01'
""")
timed("one month, partitioned (one folder read)", f"""
    SELECT SUM(amount)
    FROM read_parquet('{target}/*/*.parquet', hive_partitioning = true)
    WHERE status = 'paid' AND order_month = '2025-06'
""")
