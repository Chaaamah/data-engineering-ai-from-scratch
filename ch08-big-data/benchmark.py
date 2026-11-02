"""Exercise 8.1: total paid revenue with pandas, DuckDB and PySpark.

Run make_orders.py first. Engines that are not installed are skipped.
"""
import time
from pathlib import Path

DATA = Path(__file__).parent / "data"
CSV, PARQUET = DATA / "orders.csv", DATA / "orders.parquet"


def timed(label, fn):
    t0 = time.perf_counter()
    try:
        value = fn()
    except ImportError as exc:
        reason = f"{exc.name} not installed" if exc.name else str(exc).splitlines()[0][:70]
        print(f"{label:<24} skipped ({reason})")
        return
    except FileNotFoundError as exc:
        print(f"{label:<24} skipped ({exc.filename} not found)")
        return
    print(f"{label:<24} {time.perf_counter() - t0:6.2f} s   revenue = {value:,.2f}")


def pandas_csv():
    import pandas as pd
    df = pd.read_csv(CSV, usecols=["amount", "status"])
    return df.loc[df["status"] == "paid", "amount"].sum()


def pandas_parquet():
    import pandas as pd
    df = pd.read_parquet(PARQUET, columns=["amount", "status"])   # column pruning
    return df.loc[df["status"] == "paid", "amount"].sum()


def duckdb_query(path):
    import duckdb
    return duckdb.sql(f"SELECT SUM(amount) FROM '{path}' WHERE status = 'paid'").fetchone()[0]


def spark_parquet():
    from pyspark.sql import SparkSession, functions as F
    spark = SparkSession.builder.appName("benchmark").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.read.parquet(str(PARQUET))
    value = df.filter(F.col("status") == "paid").agg(F.sum("amount")).first()[0]
    spark.stop()
    return value


timed("pandas, CSV", pandas_csv)
timed("pandas, Parquet", pandas_parquet)
timed("DuckDB, CSV", lambda: duckdb_query(CSV))
timed("DuckDB, Parquet", lambda: duckdb_query(PARQUET))
timed("PySpark, Parquet", spark_parquet)   # includes Spark start-up time on purpose
