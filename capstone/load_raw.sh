#!/usr/bin/env bash
# Load the generated CSV files into the raw schema of the Docker database.
set -euo pipefail
cd "$(dirname "$0")"

P="docker compose exec -T postgres psql -U de_user -d warehouse -v ON_ERROR_STOP=1"
$P < sql/raw_schema.sql
for table in customers orders support_tickets; do
  $P -c "\copy raw.${table} FROM STDIN WITH (FORMAT csv, HEADER true)" < "data/${table}.csv"
done
$P -c "SELECT 'customers' AS t, COUNT(*) FROM raw.customers
       UNION ALL SELECT 'orders', COUNT(*) FROM raw.orders
       UNION ALL SELECT 'support_tickets', COUNT(*) FROM raw.support_tickets;"
