"""Chapter 8.4: daily paid revenue per city with PySpark (needs Java 17+)."""
import sys
from pathlib import Path

from pyspark.sql import SparkSession, functions as F

source = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent / "data" / "orders.parquet")
target = str(Path(__file__).parent / "data" / "daily_revenue")

spark = SparkSession.builder.appName("daily_revenue").getOrCreate()

orders = spark.read.parquet(source)

daily = (
    orders
    .filter(F.col("status") == "paid")
    .withColumn("order_date", F.to_date("ordered_at"))
    .groupBy("order_date", "city")
    .agg(
        F.sum("amount").alias("revenue"),
        F.countDistinct("customer_id").alias("customers"),
    )
)

daily.show(5)   # an action: now Spark runs the plan

(daily.write
      .mode("overwrite")
      .partitionBy("order_date")
      .parquet(target))

# The same question in Spark SQL
orders.createOrReplaceTempView("orders")
spark.sql("""
    SELECT city, SUM(amount) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY city
    ORDER BY revenue DESC
""").show()

spark.stop()
