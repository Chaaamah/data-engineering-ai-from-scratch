"""Chapter 7: the weather pipeline as an Airflow DAG with data quality checks.

Copy (or symlink) ch06-pipeline/pipelines into your Airflow dags folder so that
`from pipelines.weather import run` works, and set PG_DSN for the Airflow workers.
"""
from datetime import datetime, timedelta

from airflow.sdk import dag, task   # Airflow 2.x: from airflow.decorators import dag, task


@dag(
    schedule="0 6 * * *",              # every day at 06:00
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 3, "retry_delay": timedelta(minutes=5)},
    tags=["weather"],
)
def weather_daily():

    @task
    def extract_and_load():
        from pipelines.weather import run
        run()

    @task
    def check_quality():
        import psycopg
        from pipelines.weather import DSN

        checks = {
            "no rows loaded in the last day":
                "SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END "
                "FROM weather_hourly WHERE loaded_at > now() - interval '1 day'",
            "null temperatures":
                "SELECT COUNT(*) FROM weather_hourly WHERE temperature_c IS NULL",
            "humidity out of range":
                "SELECT COUNT(*) FROM weather_hourly "
                "WHERE humidity_pct NOT BETWEEN 0 AND 100",
            # Exercise 7.3 solution: see README.md for why it filters on past hours
            "stale observations (newest past hour older than 26 hours)":
                "SELECT CASE WHEN COALESCE(MAX(observed_at), 'epoch') "
                "< (now() AT TIME ZONE 'Africa/Casablanca') - interval '26 hours' "
                "THEN 1 ELSE 0 END FROM weather_hourly "
                "WHERE observed_at <= now() AT TIME ZONE 'Africa/Casablanca'",
        }
        failures = []
        with psycopg.connect(DSN) as conn:
            for name, sql in checks.items():
                bad = conn.execute(sql).fetchone()[0]
                if bad:
                    failures.append(f"{name}: {bad}")
        if failures:
            raise ValueError("Data quality failed: " + "; ".join(failures))

    extract_and_load() >> check_quality()


weather_daily()
