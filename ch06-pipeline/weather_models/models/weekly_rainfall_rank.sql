-- Exercise 6.3: rank cities by total rainfall per week.
WITH weekly AS (
    SELECT
        city,
        CAST(date_trunc('week', weather_date) AS DATE) AS week_start,
        SUM(precipitation_total_mm)                     AS rainfall_mm
    FROM {{ ref('daily_weather') }}
    GROUP BY city, date_trunc('week', weather_date)
)
SELECT
    week_start,
    city,
    rainfall_mm,
    RANK() OVER (PARTITION BY week_start ORDER BY rainfall_mm DESC NULLS LAST) AS rainfall_rank
FROM weekly
