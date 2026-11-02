-- Capstone: the raw layer. Data lands here exactly as extracted.
CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.support_tickets, raw.orders, raw.customers;

CREATE TABLE raw.customers (
    customer_id  INT PRIMARY KEY,
    city         TEXT,
    plan         TEXT,
    signed_up_at DATE
);

CREATE TABLE raw.orders (
    order_id    INT PRIMARY KEY,
    customer_id INT REFERENCES raw.customers(customer_id),
    ordered_at  TIMESTAMP,
    amount      NUMERIC(10, 2),
    status      TEXT
);

CREATE TABLE raw.support_tickets (
    ticket_id   INT PRIMARY KEY,
    customer_id INT REFERENCES raw.customers(customer_id),
    created_at  TIMESTAMP,
    category    TEXT
);
