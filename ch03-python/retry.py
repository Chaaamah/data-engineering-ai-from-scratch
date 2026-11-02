"""Chapter 3: logging and retries with exponential backoff."""
import logging
import time

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
log = logging.getLogger("weather")


def fetch_with_retry(url: str, params: dict, attempts: int = 3) -> dict:
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as exc:
            log.warning("Attempt %d/%d failed: %s", attempt, attempts, exc)
            if attempt == attempts:
                raise
            time.sleep(2 ** attempt)   # wait 2, 4, 8... seconds


if __name__ == "__main__":
    data = fetch_with_retry(
        "https://api.open-meteo.com/v1/forecast",
        {"latitude": 34.02, "longitude": -6.84, "hourly": "temperature_2m",
         "timezone": "Africa/Casablanca"},
    )
    log.info("Received %d hourly values", len(data["hourly"]["time"]))
