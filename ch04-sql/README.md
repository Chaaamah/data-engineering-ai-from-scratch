# Chapter 4 — SQL and relational databases

Run the files in order against the Docker database:

```bash
P="docker compose exec -T postgres psql -U de_user -d warehouse"
$P < ch04-sql/01_schema.sql            # recreates customers and orders with sample rows
$P < ch04-sql/02_queries.sql
$P < ch04-sql/03_window_functions.sql
python ch04-sql/sql_from_python.py
```

`01_schema.sql` drops and recreates the tables, so you can run it again whenever you want a clean start.

## Solutions

| Exercise | File |
| --- | --- |
| 1. Monthly revenue from paid orders | `solutions/ex1_monthly_revenue.sql` |
| 2. Days between consecutive orders | `solutions/ex2_days_between_orders.sql` |
| 3. Index benchmark on 100,000 orders | `solutions/ex3_index_benchmark.sql` |

```bash
$P < ch04-sql/solutions/ex3_index_benchmark.sql
```

Compare the two `EXPLAIN ANALYZE` plans: look at the scan type and the execution time.
