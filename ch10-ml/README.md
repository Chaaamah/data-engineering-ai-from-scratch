# Chapter 10 — Machine learning fundamentals

```bash
cd ch10-ml
python make_data.py     # 5,000 synthetic subscribers in data/customers_churn.csv
python train.py         # cross-validation, test report, saves ../model.joblib for Chapter 12
```

`churn.py` holds the shared loading and pipeline code, so the training script and the solutions use exactly the same preprocessing.

## Solutions

| Exercise | File |
| --- | --- |
| 1. Logistic regression vs random forest | `solutions/ex1_logreg_vs_rf.py` |
| 2. Share of churners in the riskiest 20% | `solutions/ex2_top20_capture.py` |
| 3. RFM features in SQL | `solutions/ex3_rfm_features.sql` |

```bash
python solutions/ex1_logreg_vs_rf.py
python solutions/ex2_top20_capture.py
docker compose exec -T postgres psql -U de_user -d warehouse < solutions/ex3_rfm_features.sql
```

On this dataset, logistic regression beats the random forest in every fold (cross-validated ROC AUC 0.749 against 0.712). That is not a bug: the data was generated from a linear formula, which is exactly what logistic regression assumes. On real data, always compare a simple baseline before reaching for a complex model.

The riskiest 20% of test customers contain about 42% of all churners, about 2 times better than calling customers at random.
