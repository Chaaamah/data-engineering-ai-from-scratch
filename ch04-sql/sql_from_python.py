"""Chapter 4.7: run a parameterised query from Python with SQLAlchemy and pandas."""
import os

import pandas as pd
from sqlalchemy import create_engine, text

dsn = os.environ.get("PG_DSN", "postgresql://de_user:de_password@localhost:5432/warehouse")
engine = create_engine(dsn.replace("postgresql://", "postgresql+psycopg://", 1))

query = text("SELECT * FROM orders WHERE status = :status ORDER BY ordered_at")
with engine.connect() as conn:
    paid = pd.read_sql(query, conn, params={"status": "paid"})   # bound parameter, never string pasting

print(paid)
