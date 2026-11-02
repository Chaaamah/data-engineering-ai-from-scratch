"""Exercise 3.3: compare the size of the same data as CSV and as Parquet.

Uses output/weather_multi_city.csv from exercise 2 when it exists,
otherwise generates a similar dataset so the comparison works offline.
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path(__file__).parents[1] / "output"
OUTPUT.mkdir(exist_ok=True)
source = OUTPUT / "weather_multi_city.csv"

if source.exists():
    df = pd.read_csv(source, parse_dates=["observed_at"])
else:
    rng = np.random.default_rng(0)
    hours = pd.date_range("2025-01-01", periods=24 * 365, freq="h")
    df = pd.concat([
        pd.DataFrame({"city": city, "observed_at": hours,
                      "temperature_c": (base + 6 * np.sin(np.arange(len(hours)) * 2 * np.pi / 24)
                                        + rng.normal(0, 1.5, len(hours))).round(1)})
        for city, base in {"Casablanca": 19, "Rabat": 18, "Fes": 17, "Agadir": 21}.items()
    ], ignore_index=True)

csv_path, parquet_path = OUTPUT / "weather.csv", OUTPUT / "weather.parquet"
df.to_csv(csv_path, index=False)
try:
    df.to_parquet(parquet_path, index=False)
except ImportError:
    raise SystemExit("Install pyarrow first: pip install pyarrow")

csv_kb, parquet_kb = csv_path.stat().st_size / 1024, parquet_path.stat().st_size / 1024
print(f"{len(df):,} rows")
print(f"CSV:     {csv_kb:8.1f} KB")
print(f"Parquet: {parquet_kb:8.1f} KB  ({csv_kb / parquet_kb:.1f}x smaller)")
print("Parquet also keeps the column types: no need for parse_dates when reading it back.")
