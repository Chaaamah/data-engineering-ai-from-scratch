"""Chapter 12.3: serve the churn model with FastAPI.

After ch10-ml/train.py has written model.joblib at the repository root:
    cd ch12-mlops
    MODEL_PATH=../model.joblib uvicorn serving.app:app --reload
Then open http://localhost:8000/docs to try requests in the browser.
"""
import os

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Churn prediction API")
model = joblib.load(os.environ.get("MODEL_PATH", "model.joblib"))


class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_spend: float = Field(ge=0)
    support_tickets: int = Field(ge=0)
    plan: str
    region: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: Customer) -> dict:
    features = pd.DataFrame([customer.model_dump()])
    probability = float(model.predict_proba(features)[0, 1])
    return {"churn_probability": round(probability, 3),
            "high_risk": probability >= 0.5}
