"""Daily weather pipeline: Open-Meteo -> raw JSON -> clean rows -> PostgreSQL."""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import psycopg
import requests

log = logging.getLogger("weather_pipeline")

API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "Casablanca": (33.57, -7.59),
    "Rabat": (34.02, -6.84),
    "Marrakech": (31.63, -8.01),
    "Fes": (34.03, -5.00),
}
RAW_DIR = Path(os.environ.get("RAW_DIR", "data/raw/weather"))
DSN = os.environ.get("PG_DSN", "postgresql://de_user:de_password@localhost:5432/warehouse")


def extract(city: str, lat: float, lon: float) -> dict:
    """Call the API and keep an untouched copy of the response."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Africa/Casablanca",
    }
    r = requests.get(API_URL, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    (RAW_DIR / f"{city.lower()}_{stamp}.json").write_text(json.dumps(payload))
    return payload


def transform(city: str, payload: dict) -> pd.DataFrame:
    """Turn the nested JSON into a clean, validated table."""
    hourly = payload["hourly"]
    df = pd.DataFrame({
        "city": city,
        "observed_at": pd.to_datetime(hourly["time"]),
        "temperature_c": hourly["temperature_2m"],
        "humidity_pct": hourly["relative_humidity_2m"],
        "precipitation_mm": hourly["precipitation"],
    })
    df = df.dropna(subset=["temperature_c"])
    df = df.drop_duplicates(subset=["city", "observed_at"])

    impossible = df[(df["temperature_c"] < -30) | (df["temperature_c"] > 60)]
    if not impossible.empty:
        raise ValueError(f"{len(impossible)} impossible temperatures for {city}")
    return df


UPSERT = """
INSERT INTO weather_hourly
    (city, observed_at, temperature_c, humidity_pct, precipitation_mm, loaded_at)
VALUES (%s, %s, %s, %s, %s, now())
ON CONFLICT (city, observed_at) DO UPDATE SET
    temperature_c    = EXCLUDED.temperature_c,
    humidity_pct     = EXCLUDED.humidity_pct,
    precipitation_mm = EXCLUDED.precipitation_mm,
    loaded_at        = now();
"""


def to_rows(df: pd.DataFrame) -> list[tuple]:
    """Plain Python values for the database driver; NaN becomes NULL."""
    clean = df.astype(object).where(df.notna(), None)
    return list(clean.itertuples(index=False, name=None))


def load(df: pd.DataFrame) -> int:
    """Upsert rows in one transaction: all rows land, or none do."""
    rows = to_rows(df)
    with psycopg.connect(DSN) as conn:          # commits on success
        with conn.cursor() as cur:
            cur.executemany(UPSERT, rows)
    return len(rows)


def run() -> None:
    total = 0
    for city, (lat, lon) in CITIES.items():
        payload = extract(city, lat, lon)
        df = transform(city, payload)
        total += load(df)
        log.info("Loaded %d rows for %s", len(df), city)
    log.info("Pipeline finished: %d rows upserted", total)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    run()
