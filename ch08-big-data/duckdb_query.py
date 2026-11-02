"""Chapter 8.6: query Parquet files directly with DuckDB, no server needed."""
from pathlib import Path

import duckdb

path = Path(__file__).parent / "data" / "orders.parquet"

result = duckdb.sql(f"""
    SELECT city, SUM(amount) AS revenue
    FROM '{path}'
    WHERE status = 'paid'
    GROUP BY city
    ORDER BY revenue DESC
""").df()   # back to pandas

print(result)
