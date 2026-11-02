-- Chapter 4: the shop schema used throughout the chapter.
-- Run: docker compose exec -T postgres psql -U de_user -d warehouse < ch04-sql/01_schema.sql

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id  SERIAL PRIMARY KEY,
    full_name    TEXT NOT NULL,
    city         TEXT,
    signed_up_at DATE NOT NULL
);

CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    ordered_at  TIMESTAMP NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    status      TEXT NOT NULL
);

INSERT INTO customers (full_name, city, signed_up_at) VALUES
    ('Salma Bennani', 'Casablanca', '2025-01-10'),
    ('Youssef Alaoui', 'Rabat', '2025-02-03'),
    ('Imane Tazi', 'Marrakech', '2025-03-15'),
    ('Omar El Idrissi', 'Fes', '2025-04-01');      -- has no orders yet

INSERT INTO orders (customer_id, ordered_at, amount, status) VALUES
    (1, '2025-03-01 10:15', 250.00, 'paid'),
    (1, '2025-04-12 18:40', 120.50, 'paid'),
    (2, '2025-04-13 09:05', 990.00, 'refunded'),
    (3, '2025-05-02 14:22', 75.00, 'paid'),
    (1, '2025-05-20 11:00', 310.00, 'paid'),
    (3, '2025-05-28 16:45', 42.90, 'paid');
