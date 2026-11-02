"""Chapter 10: a realistic synthetic churn dataset (5,000 subscribers)."""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
n = 5000
df = pd.DataFrame({
    "tenure_months": rng.integers(1, 60, n),
    "monthly_spend": rng.normal(300, 120, n).clip(20).round(2),
    "support_tickets": rng.poisson(1.5, n),
    "plan": rng.choice(["basic", "standard", "premium"], n, p=[0.5, 0.35, 0.15]),
    "region": rng.choice(["Casablanca-Settat", "Rabat-Sale-Kenitra",
                          "Marrakech-Safi", "Fes-Meknes"], n),
})
logit = (-1.0 - 0.05 * df["tenure_months"] + 0.45 * df["support_tickets"]
         - 0.002 * df["monthly_spend"] + np.where(df["plan"] == "basic", 0.6, 0.0))
df["churned"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)

df.to_csv(OUT / "customers_churn.csv", index=False)
print(f"Wrote {len(df)} rows, churn rate {df['churned'].mean():.1%}")
