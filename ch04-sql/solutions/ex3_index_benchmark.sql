-- Exercise 4.3: measure a filter before and after adding an index.
-- Run after 01_schema.sql. It adds 100,000 fake orders.

INSERT INTO orders (customer_id, ordered_at, amount, status)
SELECT
    1 + (g % 3),
    timestamp '2024-01-01' + (g % 730) * interval '1 day' + (g % 1440) * interval '1 minute',
    round((random() * 1000)::numeric, 2),
    (ARRAY['paid', 'paid', 'paid', 'refunded', 'cancelled'])[1 + (g % 5)]
FROM generate_series(1, 100000) AS g;

ANALYZE orders;

-- Before: no index on ordered_at, so PostgreSQL reads every row (Seq Scan).
DROP INDEX IF EXISTS idx_orders_ordered_at;
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE ordered_at >= '2025-06-01' AND ordered_at < '2025-06-02';

-- After: the index lets PostgreSQL jump to the matching rows (Index or Bitmap Scan).
CREATE INDEX idx_orders_ordered_at ON orders (ordered_at);
ANALYZE orders;
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE ordered_at >= '2025-06-01' AND ordered_at < '2025-06-02';

-- Lesson: an index helps when the filter is selective. One day out of two years
-- is about 0.1% of the rows. An index on customer_id would barely help here,
-- because the fake data has only 3 customers: each value matches a third of the table.
