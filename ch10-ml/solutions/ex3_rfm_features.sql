-- Exercise 10.3: recency, frequency and monetary features per customer,
-- computed "as of" a fixed date so that no future data leaks into the features.
-- Runs on the Chapter 4 shop schema (ch04-sql/01_schema.sql).

WITH params AS (
    SELECT timestamp '2025-06-01' AS as_of
),
paid AS (
    SELECT o.*
    FROM orders o, params p
    WHERE o.status = 'paid'
      AND o.ordered_at < p.as_of                 -- only what was known on as_of
)
SELECT
    c.customer_id,
    p.as_of::date - MAX(paid.ordered_at)::date                                         AS recency_days,
    COUNT(paid.order_id) FILTER (WHERE paid.ordered_at >= p.as_of - interval '90 days') AS frequency_90d,
    COALESCE(SUM(paid.amount) FILTER (WHERE paid.ordered_at >= p.as_of - interval '90 days'), 0)
                                                                                      AS monetary_90d
FROM customers c
CROSS JOIN params p
LEFT JOIN paid ON paid.customer_id = c.customer_id
GROUP BY c.customer_id, p.as_of
ORDER BY c.customer_id;

-- Customers who never ordered get recency_days = NULL. Before training, replace it
-- with a large value (for example 999) and add a flag column "has_ordered".
