"""Exercise 12.1 (part 1): register a run's model and point the "champion" alias at it.

usage: python ex1_register_model.py <run_id>     (train_tracked.py prints the best run id)
"""
import os
import sys

import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
run_id = sys.argv[1]

version = mlflow.register_model(f"runs:/{run_id}/model", "churn")
MlflowClient().set_registered_model_alias("churn", "champion", version.version)
print(f"churn version {version.version} is now 'champion'")
print("Serve it with: MODEL_URI=models:/churn@champion uvicorn solutions.app_registered:app")
