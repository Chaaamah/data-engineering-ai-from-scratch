-- Exercise 5.3: apply a Type 2 change when Salma (customer_id = 1)
-- moves from Casablanca to Tangier on 2025-10-01.
-- Run after ../star_schema.sql.

BEGIN;

-- 1. Close the current row
UPDATE dim_customer
SET valid_to = date '2025-09-30',
    is_current = false
WHERE customer_id = 1
  AND is_current;

-- 2. Insert the new version with a new surrogate key
INSERT INTO dim_customer (customer_id, full_name, city, valid_from, valid_to, is_current)
SELECT customer_id, full_name, 'Tangier', date '2025-10-01', NULL, true
FROM dim_customer
WHERE customer_id = 1
  AND valid_to = date '2025-09-30';

COMMIT;

-- Both statements run in one transaction: a reader never sees zero or two current rows.
SELECT customer_key, customer_id, city, valid_from, valid_to, is_current
FROM dim_customer
WHERE customer_id = 1
ORDER BY valid_from;

-- When loading a fact, pick the version that was valid on the order date:
--   JOIN dim_customer c
--     ON c.customer_id = src.customer_id
--    AND src.order_date >= c.valid_from
--    AND (c.valid_to IS NULL OR src.order_date <= c.valid_to)
