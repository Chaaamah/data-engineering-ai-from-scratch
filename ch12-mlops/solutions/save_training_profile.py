"""Exercise 12.2: store the training data's statistics next to the model version."""
import os
import sys
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).parents[2] / "ch10-ml"))
from churn import NUMERIC, load_split  # noqa: E402

DSN = os.environ.get("PG_DSN", "postgresql://de_user:de_password@localhost:5432/warehouse")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "joblib-local")

X_train, *_ = load_split()
rows = [(MODEL_VERSION, f, float(X_train[f].mean()), float(X_train[f].std())) for f in NUMERIC]

with psycopg.connect(DSN) as conn:
    conn.cursor().executemany(
        """INSERT INTO training_profile (model_version, feature, mean, stddev)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (model_version, feature) DO UPDATE
           SET mean = EXCLUDED.mean, stddev = EXCLUDED.stddev""",
        rows,
    )
for r in rows:
    print(f"{r[1]:<16} mean {r[2]:8.2f}  std {r[3]:8.2f}")
