-- Chapter 6: destination table. The primary key makes the upsert possible.
CREATE TABLE IF NOT EXISTS weather_hourly (
    city             TEXT          NOT NULL,
    observed_at      TIMESTAMP     NOT NULL,   -- local time, Africa/Casablanca
    temperature_c    NUMERIC(5, 2) NOT NULL,
    humidity_pct     NUMERIC(5, 2),
    precipitation_mm NUMERIC(6, 2),
    loaded_at        TIMESTAMPTZ   NOT NULL,
    PRIMARY KEY (city, observed_at)
);
