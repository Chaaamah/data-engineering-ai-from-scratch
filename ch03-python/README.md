# Chapter 3 — Python for data work

| File | What it shows |
| --- | --- |
| `pandas_essentials.py` | Loading, inspecting, cleaning, aggregating and joining the sample orders |
| `weather_api.py` | Calling the Open-Meteo API with a timeout and error handling |
| `retry.py` | Logging and retries with exponential backoff |
| `data/orders.csv` | 15 sample orders with deliberate problems to find and fix |
| `data/customers.csv` | Customers to join with the orders |

```bash
python ch03-python/pandas_essentials.py
python ch03-python/weather_api.py      # needs internet access
python ch03-python/retry.py            # needs internet access
```

The sample orders contain six kinds of problems on purpose: a missing amount, a duplicated row, a repeated order ID, city names with stray spaces and mixed letter case, a negative amount and one extreme value. Can you find them all before running the solution?

## Solutions

| Exercise | File |
| --- | --- |
| 1. Profile a CSV and list its quality problems | `solutions/ex1_profile_csv.py` |
| 2. Weather for four cities in one DataFrame | `solutions/ex2_multi_city.py` |
| 3. Compare CSV and Parquet sizes | `solutions/ex3_csv_vs_parquet.py` |

```bash
python ch03-python/solutions/ex1_profile_csv.py                 # profiles data/orders.csv
python ch03-python/solutions/ex1_profile_csv.py path/to/any.csv # or any CSV you like
```
