# Chapter 1 — Model answers

These exercises have no single right answer. Use these as a reference for the level of detail to aim for.

## 1. Five kinds of data from a food delivery app

| Data | Example record | Batch or streaming? | Why |
| --- | --- | --- | --- |
| Orders | order 9812, 3 items, 186 MAD, restaurant 44 | Both | Streaming for the live kitchen and driver flow; batch for daily revenue reports |
| Courier GPS positions | courier 211 at 33.589, -7.603, 12:04:31 | Streaming | Customers watch the courier move; delays of minutes are useless |
| Payments | card payment of 186 MAD, approved | Streaming for fraud checks, batch for finance | Fraud must be stopped before the order is accepted; accounting closes daily |
| Ratings and reviews | 4 stars, "food arrived cold" | Batch | Nobody needs them within seconds; nightly sentiment analysis is enough |
| App clicks | user opened the "pizza" category | Batch, sometimes streaming | Product analytics is daily; real-time recommendations would need streaming |

The pattern to notice: **streaming is justified when a decision must be taken while the event is still happening**.

## 2. Mapping job postings to lifecycle stages

Take each tool name and ask "which stage does this serve?". A typical result:

| Tool in the posting | Lifecycle stage |
| --- | --- |
| Python, SQL | Every stage |
| Kafka, Airbyte, Fivetran | Ingestion |
| Snowflake, BigQuery, S3, Delta Lake | Storage |
| dbt, Spark | Transformation |
| Airflow, Dagster | Orchestration (undercurrent) |
| Power BI, Tableau, Looker | Serving |
| Great Expectations, Soda | Data quality (undercurrent) |

Most postings ask for the same five skills: SQL, Python, one cloud warehouse, one orchestrator and one transformation tool.

## 3. Why a smarter model cannot fix bad data

> A machine learning model learns patterns from examples. If the examples contain duplicated orders, wrong labels or missing values, the model learns those mistakes as if they were true. A more powerful model learns them even more faithfully. Cleaning, deduplicating and validating the data removes the mistakes at their source, so every model trained on it improves at once.
