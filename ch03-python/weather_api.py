"""Chapter 3: call the free Open-Meteo API (no key needed)."""
import requests

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 33.57,
    "longitude": -7.59,
    "hourly": "temperature_2m",
    "timezone": "Africa/Casablanca",
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()      # stop if the server returned an error
payload = response.json()

hourly = payload["hourly"]
print(hourly["time"][:3], hourly["temperature_2m"][:3])
