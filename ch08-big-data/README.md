# Chapter 8 — Big data and distributed processing

```bash
python ch08-big-data/make_orders.py              # 5 million orders, about 300 MB of CSV
python ch08-big-data/make_orders.py --rows 500000  # a smaller run for slow laptops
python ch08-big-data/benchmark.py
python ch08-big-data/duckdb_query.py
python ch08-big-data/spark_daily_revenue.py      # needs Java 17+ and pyspark
```

Generated files go to `ch08-big-data/data/`, which is git-ignored.

## Solutions

### Exercise 1 — pandas vs DuckDB vs PySpark

`benchmark.py` times the same question with each engine. What you should observe:

- Reading **Parquet** is several times faster than CSV for every engine, because only two columns are read and no text parsing is needed.
- **DuckDB** is usually the fastest on one machine: it is columnar, multi-threaded and streams the file instead of loading it all into memory.
- **PySpark** is often the *slowest* at this size, because starting the JVM and planning the job cost seconds. Spark wins when the data no longer fits on one machine, not before.

### Exercise 2 — Partition by month

See `solutions/ex2_partition_by_month.py`. The partitioned query reads one folder out of 24, so it touches about 4% of the data. Partition pruning saves more as the dataset grows.

### Exercise 3 — Why is a shuffle expensive?

A shuffle moves rows between machines so that all rows with the same key end up together, for a `groupBy` or a `join`. It is expensive because:

1. every row is **serialized**, sent over the **network** and written to **disk** on the receiving side;
2. the next stage cannot start until the shuffle finishes, so the slowest machine sets the pace.

A **skewed key** makes it worse. If one customer owns 30% of the orders, the machine that receives that key does 30% of the work alone while the others wait. Common fixes are filtering early, broadcasting small tables in joins, and "salting" the hot key by splitting it into several sub-keys.
