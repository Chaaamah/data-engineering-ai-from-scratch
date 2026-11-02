"""Shared pieces for Chapter 10: load the data and build the model pipeline."""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA = Path(__file__).parent / "data" / "customers_churn.csv"
NUMERIC = ["tenure_months", "monthly_spend", "support_tickets"]
CATEGORICAL = ["plan", "region"]


def load_split():
    df = pd.read_csv(DATA)
    X = df.drop(columns=["churned"])
    y = df["churned"]
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


def preprocess() -> ColumnTransformer:
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])


def random_forest() -> Pipeline:
    return Pipeline([
        ("preprocess", preprocess()),
        ("classifier", RandomForestClassifier(
            n_estimators=300, min_samples_leaf=5,
            class_weight="balanced", random_state=42)),
    ])
