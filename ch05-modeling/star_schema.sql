-- Chapter 5: a star schema for order lines, with a little sample data.

DROP TABLE IF EXISTS fact_order_line, dim_date, dim_customer, dim_product;

CREATE TABLE dim_date (
    date_key     INT PRIMARY KEY,        -- e.g. 20250412
    full_date    DATE NOT NULL,
    year         INT,
    month        INT,
    month_name   TEXT,
    day_of_week  TEXT,
    is_weekend   BOOLEAN
);

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,     -- surrogate key
    customer_id  INT NOT NULL,           -- natural key from the source
    full_name    TEXT,
    city         TEXT,
    valid_from   DATE NOT NULL,
    valid_to     DATE,
    is_current   BOOLEAN NOT NULL
);

CREATE TABLE dim_product (
    product_key  SERIAL PRIMARY KEY,
    product_id   INT NOT NULL,
    product_name TEXT,
    category     TEXT
);

CREATE TABLE fact_order_line (
    order_id     INT NOT NULL,
    line_number  INT NOT NULL,
    date_key     INT REFERENCES dim_date(date_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key  INT REFERENCES dim_product(product_key),
    quantity     INT,
    unit_price   NUMERIC(10, 2),
    line_total   NUMERIC(12, 2),
    PRIMARY KEY (order_id, line_number)
);

-- Sample data -----------------------------------------------------------------
INSERT INTO dim_date (date_key, full_date, year, month, month_name, day_of_week, is_weekend)
SELECT to_char(d, 'YYYYMMDD')::int, d::date,
       EXTRACT(YEAR FROM d)::int, EXTRACT(MONTH FROM d)::int,
       trim(to_char(d, 'Month')), trim(to_char(d, 'Day')),
       EXTRACT(ISODOW FROM d) IN (6, 7)
FROM generate_series(date '2025-01-01', date '2025-12-31', interval '1 day') AS d;

INSERT INTO dim_customer (customer_id, full_name, city, valid_from, valid_to, is_current) VALUES
    (1, 'Salma Bennani', 'Casablanca', '2025-01-10', NULL, true),
    (2, 'Youssef Alaoui', 'Rabat', '2025-02-03', NULL, true);

INSERT INTO dim_product (product_id, product_name, category) VALUES
    (10, 'Argan oil 100 ml', 'Beauty'),
    (11, 'Mint tea 250 g', 'Grocery'),
    (12, 'Tajine pot', 'Home');

INSERT INTO fact_order_line VALUES
    (5001, 1, 20250301, 1, 1, 2, 120.00, 240.00),
    (5001, 2, 20250301, 1, 2, 1, 35.00, 35.00),
    (5002, 1, 20250412, 2, 3, 1, 260.00, 260.00),
    (5003, 1, 20250413, 1, 2, 3, 35.00, 105.00);

-- The business question becomes a simple, predictable query -----------------
SELECT d.year, d.month_name, p.category, SUM(f.line_total) AS revenue
FROM fact_order_line f
JOIN dim_date d    ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY d.year, d.month, d.month_name, p.category
ORDER BY d.year, d.month, revenue DESC;
