-- models/daily_weather.sql
SELECT
    city,
    CAST(observed_at AS DATE)       AS weather_date,
    ROUND(MIN(temperature_c), 1)    AS temp_min_c,
    ROUND(MAX(temperature_c), 1)    AS temp_max_c,
    ROUND(AVG(humidity_pct), 1)     AS humidity_avg_pct,
    ROUND(SUM(precipitation_mm), 1) AS precipitation_total_mm
FROM {{ source('raw', 'weather_hourly') }}
GROUP BY city, CAST(observed_at AS DATE)
