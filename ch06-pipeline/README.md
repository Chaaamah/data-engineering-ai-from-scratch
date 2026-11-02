# Chapter 6 — ETL and ELT: your first pipeline

## Run the pipeline

```bash
docker compose exec -T postgres psql -U de_user -d warehouse < ch06-pipeline/sql/weather_hourly.sql

python ch06-pipeline/pipelines/weather.py
python ch06-pipeline/pipelines/weather.py      # run it twice on purpose

docker compose exec postgres psql -U de_user -d warehouse \
  -c "SELECT city, COUNT(*) FROM weather_hourly GROUP BY city;"
```

The counts do not double: the upsert makes the pipeline idempotent.

## Test the transform step (no internet, no database)

```bash
pytest ch06-pipeline/tests
```

## Transform in the warehouse with dbt

Install dbt in its own virtual environment, because its dependencies are large:

```bash
python3 -m venv .venv-dbt && source .venv-dbt/bin/activate
pip install dbt-postgres
cd ch06-pipeline/weather_models
cp profiles.yml.example profiles.yml
dbt run  --profiles-dir .
dbt test --profiles-dir .
```

## Solutions

### Exercise 1 — Add a fifth city

Add one line to `CITIES` in `pipelines/weather.py`:

```python
"Tangier": (35.76, -5.83),
```

Run the pipeline twice. Tangier gets its rows on the first run, and the second run changes no counts. The primary key `(city, observed_at)` keeps each city's hours separate, so adding a city cannot create duplicates.

### Exercise 2 — Fetch 7 past days instead of 1

Set `"past_days": 7`. Hours that already exist hit the `ON CONFLICT` clause and are **updated** in place: their values are refreshed and `loaded_at` moves to now. Hours that did not exist are inserted. Nothing is duplicated.

This is also how you backfill: widen the window and rerun. It works only because the load is an upsert.

### Exercise 3 — Rank cities by weekly rainfall

See `weather_models/models/weekly_rainfall_rank.sql`. `RANK()` gives equal ranks to ties, and `NULLS LAST` keeps cities with missing rain data at the bottom. `dbt run` builds it after `daily_weather` automatically, because the model refers to it with `ref()`.
