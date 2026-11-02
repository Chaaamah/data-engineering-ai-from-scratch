"""Exercise 12.1 (part 2): serve whatever model version the registry calls "champion".

Promoting a new model becomes one alias change in MLflow, with no code change and no
file copied by hand. Restart the service to pick up the new version.

    cd ch12-mlops
    MLFLOW_TRACKING_URI=http://127.0.0.1:5000 MODEL_URI=models:/churn@champion \
        uvicorn solutions.app_registered:app --reload
"""
import os

import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
MODEL_URI = os.environ.get("MODEL_URI", "models:/churn@champion")

app = FastAPI(title="Churn prediction API (registry)")
model = mlflow.sklearn.load_model(MODEL_URI)


class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_spend: float = Field(ge=0)
    support_tickets: int = Field(ge=0)
    plan: str
    region: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": MODEL_URI}


@app.post("/predict")
def predict(customer: Customer) -> dict:
    probability = float(model.predict_proba(pd.DataFrame([customer.model_dump()]))[0, 1])
    return {"churn_probability": round(probability, 3), "high_risk": probability >= 0.5}
