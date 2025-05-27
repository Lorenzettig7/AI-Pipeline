from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import joblib
import pandas as pd
import os

app = FastAPI()

# Prometheus metrics
predict_counter = Counter("predict_requests_total", "Total prediction requests")
error_counter = Counter("predict_errors_total", "Total failed prediction requests")

# Load the trained model
MODEL_PATH = "model.joblib"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# Pydantic model
class InferenceInput(BaseModel):
    features: list

# Column names used during training (extracted from cleaned_ddos.csv)
columns = ['Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
           'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
           'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
           'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
           'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
           'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
           'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
           'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
           'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
           'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
           'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
           'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count',
           'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count',
           'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
           'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
           'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets',
           'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
           'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward', 'Active Mean',
           'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min']
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
        print("🔥 Prediction error:", e)  # <-- this is what’s missing
        error_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

