"""Exercise 3.2: hourly temperatures for four Moroccan cities in one DataFrame."""
from pathlib import Path

import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "Casablanca": (33.57, -7.59),
    "Rabat": (34.02, -6.84),
    "Fes": (34.03, -5.00),
    "Agadir": (30.42, -9.60),
}
OUTPUT = Path(__file__).parents[1] / "output"


def fetch(city: str, lat: float, lon: float) -> pd.DataFrame:
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m",
              "past_days": 7, "forecast_days": 1, "timezone": "Africa/Casablanca"}
    r = requests.get(URL, params=params, timeout=30)
    r.raise_for_status()
    hourly = r.json()["hourly"]
    return pd.DataFrame({
        "city": city,
        "observed_at": pd.to_datetime(hourly["time"]),
        "temperature_c": hourly["temperature_2m"],
    })


df = pd.concat([fetch(c, *coords) for c, coords in CITIES.items()], ignore_index=True)
print(df.groupby("city")["temperature_c"].agg(["count", "min", "mean", "max"]).round(1))

OUTPUT.mkdir(exist_ok=True)
df.to_csv(OUTPUT / "weather_multi_city.csv", index=False)
print(f"\nSaved {len(df)} rows to {OUTPUT / 'weather_multi_city.csv'}")
