"""Exercise 3.1: profile any CSV and list its data quality problems.

usage: python ex1_profile_csv.py [path/to/file.csv]   (default: ../data/orders.csv)
"""
import sys
from pathlib import Path

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "data" / "orders.csv"
df = pd.read_csv(path)

print(f"{path.name}: {len(df)} rows, {df.shape[1]} columns\n")
df.info()
print("\n", df.describe(include="all").T, "\n")

problems = []

# 1. Missing values
for col, n in df.isna().sum().items():
    if n:
        problems.append(f"{n} missing value(s) in '{col}'")

# 2. Fully duplicated rows
if (n := df.duplicated().sum()):
    problems.append(f"{n} fully duplicated row(s)")

# 3. Repeated values in the first column that looks like a key
keys = [c for c in df.columns if c.endswith("_id")]
if keys and (n := df[keys[0]].duplicated().sum()):
    problems.append(f"{n} repeated value(s) in key column '{keys[0]}'")

for col in df.columns:
    s = df[col].dropna()
    if is_numeric_dtype(s) and not col.endswith("_id"):
        # 4. Impossible negatives and extreme values (3 x IQR rule)
        if (neg := (s < 0).sum()):
            problems.append(f"{neg} negative value(s) in '{col}'")
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        extreme = s[(s < q1 - 3 * iqr) | (s > q3 + 3 * iqr)]
        if len(extreme):
            problems.append(f"{len(extreme)} extreme value(s) in '{col}': {sorted(extreme.tolist())}")
    elif is_string_dtype(s):
        # 5. Stray spaces and inconsistent letter case in text columns
        text = s.astype(str)
        if (text != text.str.strip()).any():
            problems.append(f"'{col}' has values with leading or trailing spaces")
        clean = text.str.strip()
        if clean.str.lower().nunique() < clean.nunique():
            problems.append(f"'{col}' writes the same value with different letter case")

print("Data quality problems found:")
for p in problems or ["none"]:
    print(" -", p)
