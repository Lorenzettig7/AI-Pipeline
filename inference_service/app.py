from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import joblib
import pandas as pd
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Prometheus metrics
predict_counter = Counter("predict_requests_total", "Total prediction requests")
error_counter = Counter("predict_errors_total", "Total failed prediction requests")

# Load the model path from environment variable or use default
MODEL_PATH = os.getenv("MODEL_FILE_PATH", "model.joblib")
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# Load feature columns from JSON file
FEATURE_CONFIG_PATH = "inference_service/feature_config.json"
if not os.path.exists(FEATURE_CONFIG_PATH):
    raise RuntimeError(f"Feature config file not found at {FEATURE_CONFIG_PATH}")
with open(FEATURE_CONFIG_PATH, 'r') as f:
    columns = json.load(f)['columns']

# Pydantic model
class InferenceInput(BaseModel):
    features: list

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InferenceInput):
    predict_counter.inc()
    try:
        df = pd.DataFrame([data.features], columns=columns)
        prediction = model.predict(df)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        error_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

