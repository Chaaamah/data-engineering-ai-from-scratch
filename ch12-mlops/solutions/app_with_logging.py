"""Exercise 12.2: the prediction API, logging every request to PostgreSQL.

    cd ch12-mlops
    MODEL_PATH=../model.joblib uvicorn solutions.app_with_logging:app --reload
"""
import os

import joblib
import pandas as pd
import psycopg
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, Field

DSN = os.environ.get("PG_DSN", "postgresql://de_user:de_password@localhost:5432/warehouse")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "joblib-local")

app = FastAPI(title="Churn prediction API with logging")
model = joblib.load(os.environ.get("MODEL_PATH", "model.joblib"))


class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_spend: float = Field(ge=0)
    support_tickets: int = Field(ge=0)
    plan: str
    region: str


def log_prediction(customer: Customer, probability: float) -> None:
    with psycopg.connect(DSN) as conn:
        conn.execute(
            """INSERT INTO prediction_log (model_version, tenure_months, monthly_spend,
                   support_tickets, plan, region, churn_probability)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (MODEL_VERSION, customer.tenure_months, customer.monthly_spend,
             customer.support_tickets, customer.plan, customer.region, round(probability, 3)),
        )


@app.post("/predict")
def predict(customer: Customer, background: BackgroundTasks) -> dict:
    probability = float(model.predict_proba(pd.DataFrame([customer.model_dump()]))[0, 1])
    background.add_task(log_prediction, customer, probability)   # logging never slows the reply
    return {"churn_probability": round(probability, 3), "high_risk": probability >= 0.5}
