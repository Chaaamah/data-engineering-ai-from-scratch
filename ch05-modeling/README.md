# Chapter 5 — Data modeling and warehousing

```bash
P="docker compose exec -T postgres psql -U de_user -d warehouse"
$P < ch05-modeling/star_schema.sql
```

The script builds the star schema, fills `dim_date` for all of 2025, adds a few sample rows and runs the revenue-by-category query.

## Solutions

### Exercise 1 — Grain and dimensions for a pharmacy

**Grain:** one row per product line on a sales receipt (one product, one receipt).

**Dimensions:** date (and time of day), product (name, active ingredient, category, prescription-only flag), store or branch, customer (when a loyalty card is used), pharmacist on duty, payment method.

**Measures in the fact table:** quantity, unit price, discount, line total, insurance share.

A common mistake is to choose "one row per receipt" as the grain. You then lose the products, and every product question needs a second table.

### Exercise 2 — Fill `dim_date` for 2025

The `INSERT ... SELECT ... FROM generate_series(...)` statement in `star_schema.sql` is the solution. Change the two dates to cover more years.

### Exercise 3 — Type 2 change when a customer moves

See `solutions/ex3_scd2_city_change.sql`. Run it after `star_schema.sql`:

```bash
$P < ch05-modeling/solutions/ex3_scd2_city_change.sql
```
