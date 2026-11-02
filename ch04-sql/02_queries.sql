-- Chapter 4: filtering, aggregations and joins.

-- 4.2 Filtering and sorting
SELECT order_id, amount, status
FROM orders
WHERE status = 'paid'
  AND amount > 100
ORDER BY amount DESC
LIMIT 10;

-- 4.3 Aggregations and GROUP BY
SELECT
    status,
    COUNT(*)              AS orders,
    SUM(amount)           AS revenue,
    ROUND(AVG(amount), 2) AS avg_order_value
FROM orders
GROUP BY status
HAVING COUNT(*) >= 1
ORDER BY revenue DESC;

-- 4.4 JOINs
SELECT c.full_name, c.city, o.ordered_at, o.amount
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status = 'paid';

-- Customers who have never ordered (Omar, in the sample data)
SELECT c.full_name
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
