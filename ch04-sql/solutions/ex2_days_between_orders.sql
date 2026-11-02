-- Exercise 4.2: days between each customer's consecutive orders.

SELECT
    customer_id,
    ordered_at,
    LAG(ordered_at) OVER w                         AS previous_order_at,
    ordered_at::date - LAG(ordered_at::date) OVER w AS days_since_previous
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY ordered_at)
ORDER BY customer_id, ordered_at;

-- The first order of each customer has no previous order, so its value is NULL.
-- Average gap per customer, a useful churn feature:
WITH gaps AS (
    SELECT customer_id,
           ordered_at::date - LAG(ordered_at::date) OVER (
               PARTITION BY customer_id ORDER BY ordered_at) AS gap_days
    FROM orders
)
SELECT customer_id, ROUND(AVG(gap_days), 1) AS avg_days_between_orders
FROM gaps
WHERE gap_days IS NOT NULL
GROUP BY customer_id
ORDER BY customer_id;
