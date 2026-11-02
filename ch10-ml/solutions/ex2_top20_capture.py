"""Exercise 10.2: what share of real churners sits in the riskiest 20% of customers?"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))
from churn import load_split, random_forest  # noqa: E402

X_train, X_test, y_train, y_test = load_split()
model = random_forest().fit(X_train, y_train)

ranked = pd.DataFrame({"risk": model.predict_proba(X_test)[:, 1], "churned": y_test.values})
ranked = ranked.sort_values("risk", ascending=False).reset_index(drop=True)

top = ranked.head(int(len(ranked) * 0.20))
captured = top["churned"].sum() / ranked["churned"].sum()
print(f"Test customers: {len(ranked)}, real churners: {ranked['churned'].sum()}")
print(f"The riskiest 20% ({len(top)} customers) contain {captured:.0%} of all churners.")
print(f"A random 20% would contain about 20%: the model is {captured / 0.20:.1f}x better than chance.")
print("\nBusiness reading: calling only the top 20% reaches"
      f" {captured:.0%} of the customers who would leave.")
