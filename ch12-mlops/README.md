# Chapter 12 — MLOps

Train the model first with `ch10-ml/train.py`; it writes `model.joblib` at the repository root.

## Serve the model

```bash
cd ch12-mlops
MODEL_PATH=../model.joblib uvicorn serving.app:app --reload
```

Open http://localhost:8000/docs, or call it from a terminal:

```bash
curl -s -X POST localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"tenure_months": 3, "monthly_spend": 150, "support_tickets": 4, "plan": "basic", "region": "Fes-Meknes"}'
```

## Package it with Docker

```bash
cd ch12-mlops
cp ../model.joblib .
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```

The image runs as a non-root user and contains only the serving code and the model.

## Track experiments with MLflow

```bash
mlflow server --host 127.0.0.1 --port 5000      # terminal 1, UI at http://127.0.0.1:5000
python ch12-mlops/train_tracked.py              # terminal 2
```

## Solutions

### Exercise 1 — Serve the registered model

```bash
python ch12-mlops/solutions/ex1_register_model.py <best_run_id>
cd ch12-mlops
MODEL_URI=models:/churn@champion uvicorn solutions.app_registered:app
```

Promoting a better model later means moving the `champion` alias to its version and restarting the service: no file copied by hand, and a full history of which version served when.

### Exercise 2 — Log predictions and watch for drift

```bash
docker compose exec -T postgres psql -U de_user -d warehouse < ch12-mlops/solutions/prediction_log.sql
python ch12-mlops/solutions/save_training_profile.py
cd ch12-mlops && MODEL_PATH=../model.joblib uvicorn solutions.app_with_logging:app
```

Send some requests, then re-run the drift query at the end of `prediction_log.sql`. A `z_score` beyond ±2 means this week's customers look different from the training data: investigate before trusting the predictions.

### Exercise 3 — The capstone

See the [`capstone`](../capstone) folder.
