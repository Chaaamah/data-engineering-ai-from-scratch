-- Exercise 4.1: monthly revenue from paid orders, one row per month.

SELECT
    date_trunc('month', ordered_at)::date AS month,
    COUNT(*)                              AS paid_orders,
    SUM(amount)                           AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY date_trunc('month', ordered_at)
ORDER BY month;

-- Months with no paid orders do not appear. To show them with 0, join to a
-- generated list of months:
WITH months AS (
    SELECT generate_series(date '2025-03-01', date '2025-06-01', interval '1 month')::date AS month
)
SELECT m.month,
       COUNT(o.order_id)           AS paid_orders,
       COALESCE(SUM(o.amount), 0)  AS revenue
FROM months AS m
LEFT JOIN orders AS o
       ON date_trunc('month', o.ordered_at) = m.month
      AND o.status = 'paid'
GROUP BY m.month
ORDER BY m.month;
