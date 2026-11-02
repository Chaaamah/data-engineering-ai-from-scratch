# Chapter 7 — Orchestration and data quality

## Run Airflow locally

Install Airflow in its own virtual environment with the official constraints file, which pins compatible versions of its many dependencies:

```bash
python3 -m venv .venv-airflow && source .venv-airflow/bin/activate
AIRFLOW_VERSION=3.0.6
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
pip install "apache-airflow==${AIRFLOW_VERSION}" psycopg[binary] pandas requests \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

export AIRFLOW_HOME=~/airflow
mkdir -p $AIRFLOW_HOME/dags
cp ch07-orchestration/dags/weather_daily.py $AIRFLOW_HOME/dags/
cp -r ch06-pipeline/pipelines $AIRFLOW_HOME/dags/
airflow standalone          # prints the admin password; open http://localhost:8080
```

Check the [Airflow installation page](https://airflow.apache.org/docs/apache-airflow/stable/installation/) for the latest 3.x version and replace `AIRFLOW_VERSION` if a newer one exists.

## Solutions

### Exercise 1 — Deploy and trigger the DAG

After `airflow standalone` starts, open the web interface, find `weather_daily`, switch it on and press the trigger button. Both tasks should turn green. Open each task's log to see the "Loaded N rows" messages.

### Exercise 2 — Watch the retries

Change `API_URL` in `pipelines/weather.py` to a wrong address, such as `https://api.open-meteo.com/v1/wrong`, and trigger the DAG again. The task log shows the HTTP error, then the task waits 5 minutes and retries, up to 3 times, before failing. Downstream, `check_quality` never runs. Restore the URL afterwards.

### Exercise 3 — Freshness check

The solution is the fourth check in `dags/weather_daily.py`. Two details matter:

1. **The pipeline also loads forecast hours.** `MAX(observed_at)` is therefore usually *in the future*, and a naive freshness check would always pass. The query only looks at hours up to now.
2. **`observed_at` is stored as local time without a time zone**, while `now()` returns a time-zone-aware value. Converting with `now() AT TIME ZONE 'Africa/Casablanca'` compares like with like.
