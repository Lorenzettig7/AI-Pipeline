from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb
import pandas as pd
import joblib
import os

app = FastAPI()

# Define input data model
class InferenceInput(BaseModel):
    features: list

# Load model (assumes model is saved locally as 'model.bst')
MODEL_PATH = "model.bst"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model file not found. Please download and place 'model.bst' in the working directory.")

booster = xgb.Booster()
booster.load_model(MODEL_PATH)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InferenceInput):
    try:
        dmatrix = xgb.DMatrix(pd.DataFrame([data.features]))
        prediction = booster.predict(dmatrix)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

