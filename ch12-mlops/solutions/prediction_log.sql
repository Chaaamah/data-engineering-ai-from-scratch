-- Exercise 12.2: log every prediction, then compare live inputs with the training data.

CREATE TABLE IF NOT EXISTS prediction_log (
    id                BIGSERIAL PRIMARY KEY,
    predicted_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    model_version     TEXT NOT NULL,
    tenure_months     INT,
    monthly_spend     NUMERIC(10, 2),
    support_tickets   INT,
    plan              TEXT,
    region            TEXT,
    churn_probability NUMERIC(5, 3) NOT NULL
);

-- Statistics of the training data, written once per training run
-- by save_training_profile.py.
CREATE TABLE IF NOT EXISTS training_profile (
    model_version TEXT NOT NULL,
    feature       TEXT NOT NULL,
    mean          NUMERIC,
    stddev        NUMERIC,
    PRIMARY KEY (model_version, feature)
);

-- Drift check: this week's average monthly_spend against the training data.
-- A shift of more than 2 standard errors is unlikely to be chance.
WITH live AS (
    SELECT model_version,
           AVG(monthly_spend) AS live_mean,
           COUNT(*)           AS n
    FROM prediction_log
    WHERE predicted_at >= now() - interval '7 days'
    GROUP BY model_version
)
SELECT l.model_version,
       l.n                                             AS predictions_this_week,
       ROUND(t.mean, 2)                                AS training_mean,
       ROUND(l.live_mean, 2)                           AS live_mean,
       ROUND(((l.live_mean - t.mean) / (t.stddev / sqrt(l.n)))::numeric, 1) AS z_score,
       ABS((l.live_mean - t.mean) / (t.stddev / sqrt(l.n))) > 2               AS drift_suspected
FROM live l
JOIN training_profile t
  ON t.model_version = l.model_version
 AND t.feature = 'monthly_spend';
