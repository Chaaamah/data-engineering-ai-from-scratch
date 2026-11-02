-- Chapter 4.5: window functions and CTEs.

SELECT
    customer_id,
    ordered_at,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id ORDER BY ordered_at
    ) AS running_total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id ORDER BY ordered_at DESC
    ) AS recency_rank,
    LAG(ordered_at) OVER (
        PARTITION BY customer_id ORDER BY ordered_at
    ) AS previous_order_at
FROM orders
ORDER BY customer_id, ordered_at;

-- Each customer's latest order: the deduplication pattern you will use constantly
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_at DESC) AS rn
    FROM orders
)
SELECT customer_id, ordered_at AS last_order_at, amount
FROM ranked
WHERE rn = 1
ORDER BY customer_id;
