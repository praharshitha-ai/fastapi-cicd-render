from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Linear Regression API")


# -----------------------------
# Health check endpoint (fixes 404 test failure)
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "ok"}


# -----------------------------
# Load model (clean path handling)
# -----------------------------
MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/model.pkl"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://git-cicd-1-ngtw.onrender.com"],  # Streamlit frontend on Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")


# -----------------------------
# Input schema (fixed typo: InoutData → InputData)
# -----------------------------
class InputData(BaseModel):
    area: float
    bedrooms: int


# -----------------------------
# Prediction endpoint
# -----------------------------
@app.post("/predict")
def predict(data: InputData):
    x = np.array([[data.area, data.bedrooms]])
    prediction = model.predict(x)[0]
    return {"predicted_price": float(prediction)}
