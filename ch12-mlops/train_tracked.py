"""Chapter 12.2: track every training run with MLflow, then register the best model.

Start the tracking server first, from the repository root:
    mlflow server --host 127.0.0.1 --port 5000
Then: python ch12-mlops/train_tracked.py
"""
import os
import sys
from pathlib import Path

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parents[1] / "ch10-ml"))
from churn import load_split, random_forest  # noqa: E402

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
mlflow.set_experiment("churn")

X_train, X_test, y_train, y_test = load_split()
best = {"auc": -1.0, "run_id": None}

for n_trees in [100, 300, 600]:
    with mlflow.start_run() as run:
        model = random_forest()
        model.set_params(classifier__n_estimators=n_trees)
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_param("n_estimators", n_trees)
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(
            model, "model",
            signature=infer_signature(X_train, model.predict_proba(X_train)[:, 1]),
            input_example=X_train.head(3),
        )
        print(f"n_estimators={n_trees:<4} ROC AUC {auc:.3f}  run {run.info.run_id}")
        if auc > best["auc"]:
            best = {"auc": auc, "run_id": run.info.run_id}

print(f"\nBest run {best['run_id']} with ROC AUC {best['auc']:.3f}")
print("Register it with:  python ch12-mlops/solutions/ex1_register_model.py", best["run_id"])
