"""Capstone: generate two years of fake shop data with a real churn signal.

5,000 customers, about 50,000 orders and 3,000 support tickets, written as CSV to
capstone/data/. Customers with many support tickets are more likely to stop ordering,
so the churn model in the capstone has a genuine pattern to find.
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)

START, END = pd.Timestamp("2024-11-01"), pd.Timestamp("2026-10-31")
SPAN_DAYS = (END - START).days
N_CUSTOMERS, N_TICKETS, TARGET_ORDERS = 5000, 3000, 50_000

cities = ["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier", "Agadir", "Meknes", "Oujda"]
customers = pd.DataFrame({
    "customer_id": np.arange(1, N_CUSTOMERS + 1),
    "city": rng.choice(cities, N_CUSTOMERS, p=[.30, .15, .14, .12, .11, .08, .05, .05]),
    "plan": rng.choice(["basic", "standard", "premium"], N_CUSTOMERS, p=[.55, .32, .13]),
    "signed_up_at": START + pd.to_timedelta(rng.integers(0, SPAN_DAYS - 60, N_CUSTOMERS), unit="D"),
})

# Support tickets: a quarter of customers write most of them
heavy = rng.random(N_CUSTOMERS) < 0.25
weights = np.where(heavy, 6.0, 1.0)
ticket_owner = rng.choice(customers["customer_id"], N_TICKETS, p=weights / weights.sum())
tickets_per_customer = pd.Series(ticket_owner).value_counts()
customers["n_tickets"] = customers["customer_id"].map(tickets_per_customer).fillna(0).astype(int)

# Churn: more tickets and the basic plan raise the chance of stopping
logit = -1.4 + 0.45 * customers["n_tickets"] + np.where(customers["plan"] == "basic", 0.5, -0.2)
churns = rng.random(N_CUSTOMERS) < 1 / (1 + np.exp(-logit))
active_days = (END - customers["signed_up_at"]).dt.days.to_numpy()
stop_after = np.where(churns, rng.uniform(0.2, 0.8, N_CUSTOMERS) * active_days, active_days)
customers["last_active_at"] = customers["signed_up_at"] + pd.to_timedelta(stop_after.astype(int), unit="D")

# Orders: each customer orders at their own rate while active
rate = np.array([rng.gamma(2.0, 1.0) * {"basic": 0.8, "standard": 1.0, "premium": 1.5}[p]
                 for p in customers["plan"]])
expected = rate * stop_after
n_orders = rng.poisson(expected * TARGET_ORDERS / expected.sum())

rows = []
for cid, signed, days, k in zip(customers["customer_id"], customers["signed_up_at"], stop_after, n_orders):
    if k == 0:
        continue
    offsets = np.sort(rng.uniform(0, max(days, 1), k))
    rows.append(pd.DataFrame({"customer_id": cid,
                              "ordered_at": signed + pd.to_timedelta(offsets * 86400, unit="s")}))
orders = pd.concat(rows, ignore_index=True).sort_values("ordered_at", ignore_index=True)
orders.insert(0, "order_id", np.arange(1, len(orders) + 1))
orders["ordered_at"] = orders["ordered_at"].dt.floor("min")
orders["amount"] = rng.gamma(2.2, 110.0, len(orders)).round(2)
orders["status"] = rng.choice(["paid", "refunded", "cancelled"], len(orders), p=[.91, .05, .04])

ticket_times = []
lookup = customers.set_index("customer_id")
for cid in ticket_owner:
    c = lookup.loc[cid]
    span = max((c["last_active_at"] - c["signed_up_at"]).days, 1)
    ticket_times.append(c["signed_up_at"] + pd.Timedelta(days=float(rng.uniform(0, span))))
tickets = pd.DataFrame({
    "ticket_id": np.arange(1, N_TICKETS + 1),
    "customer_id": ticket_owner,
    "created_at": pd.to_datetime(ticket_times).floor("min"),
    "category": rng.choice(["late delivery", "damaged item", "refund", "payment", "account"], N_TICKETS),
}).sort_values("created_at", ignore_index=True)

customers.drop(columns=["n_tickets", "last_active_at"]).to_csv(OUT / "customers.csv", index=False)
orders.to_csv(OUT / "orders.csv", index=False)
tickets.to_csv(OUT / "support_tickets.csv", index=False)

print(f"customers:       {len(customers):>6,}")
print(f"orders:          {len(orders):>6,}")
print(f"support tickets: {len(tickets):>6,}")
print(f"customers who stop ordering before the end: {churns.mean():.0%}")
