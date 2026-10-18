"""Train the linear regression model and save it to backend/models/model.pkl."""

import pickle
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

BACKEND_DIR = Path(__file__).resolve().parent
DATA_PATH = BACKEND_DIR.parent / "data" / "data.csv"
MODEL_PATH = BACKEND_DIR / "models" / "model.pkl"

df = pd.read_csv(DATA_PATH)
X = df[["area", "bedrooms"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

MODEL_PATH.parent.mkdir(exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
print(f"Saved model to {MODEL_PATH}")
