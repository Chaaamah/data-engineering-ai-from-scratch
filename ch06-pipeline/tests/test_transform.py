"""Offline tests for the transform step: no API call, no database.

Run from the repository root:  pytest ch06-pipeline/tests
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
pytest.importorskip("psycopg")            # the pipeline module imports it
from pipelines.weather import to_rows, transform  # noqa: E402


def payload(temps, humidity=None, rain=None):
    n = len(temps)
    return {"hourly": {
        "time": [f"2026-03-12T{h:02d}:00" for h in range(n)],
        "temperature_2m": temps,
        "relative_humidity_2m": humidity or [70] * n,
        "precipitation": rain or [0.0] * n,
    }}


def test_drops_missing_temperatures():
    df = transform("Rabat", payload([14.2, None, 13.8]))
    assert len(df) == 2
    assert df["temperature_c"].notna().all()


def test_removes_duplicate_hours():
    p = payload([14.2, 13.8])
    p["hourly"]["time"][1] = p["hourly"]["time"][0]        # the same hour twice
    assert len(transform("Rabat", p)) == 1


def test_rejects_impossible_temperatures():
    with pytest.raises(ValueError, match="impossible"):
        transform("Fes", payload([14.0, 75.0]))


def test_rows_use_none_for_missing_values():
    rows = to_rows(transform("Fes", payload([9.5], rain=[None])))
    assert rows[0][0] == "Fes"
    assert rows[0][4] is None                            # precipitation -> NULL
