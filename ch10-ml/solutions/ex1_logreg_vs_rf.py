"""Exercise 10.1: logistic regression versus random forest, judged fairly."""
import sys
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).parents[1]))
from churn import load_split, preprocess, random_forest  # noqa: E402

X_train, _, y_train, _ = load_split()
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)   # same folds for both

models = {
    "logistic regression": Pipeline([
        ("preprocess", preprocess()),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ]),
    "random forest": random_forest(),
}
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")
    results[name] = scores
    print(f"{name:<20} ROC AUC {scores.mean():.3f} ± {scores.std():.3f}")

diff = results["logistic regression"] - results["random forest"]
print(f"\nPer-fold difference (logreg - forest): {diff.round(3)}")
spread = max(s.std() for s in results.values())
print(f"Mean difference {diff.mean():+.3f}, fold-to-fold spread of a single model about ±{spread:.3f}")

if abs(diff.mean()) > spread and ((diff > 0).all() or (diff < 0).all()):
    winner = "logistic regression" if diff.mean() > 0 else "random forest"
    print(f"Verdict: {winner} wins in every fold by more than the spread, so the difference is real.")
else:
    print("Verdict: the difference is within the noise. The models are practically tied:"
          " prefer the simpler, faster and more explainable one.")
