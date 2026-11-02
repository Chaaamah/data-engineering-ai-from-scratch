"""Chapter 10.5: train and evaluate the churn model, then save it for Chapter 12."""
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score

from churn import load_split, random_forest

X_train, X_test, y_train, y_test = load_split()
model = random_forest()

# 10.6 Cross-validation on the training data only; the test set stays locked away
scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
print(f"Cross-validated ROC AUC: {scores.mean():.3f} ± {scores.std():.3f}")

model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
print(classification_report(y_test, model.predict(X_test)))
print("Test ROC AUC:", round(roc_auc_score(y_test, proba), 3))

out = Path(__file__).parents[1] / "model.joblib"
joblib.dump(model, out)
print(f"Saved {out}")
