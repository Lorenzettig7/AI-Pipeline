# This script loads the ML model (`model.joblib`) and prints the number of
# features it expects as input. It also optionally attempts a dummy prediction.
#
# Usage:
# 1. Ensure the model file `model.joblib` exists in the `inference_service/` directory.
# 2. Run this script from the repository root: `python scripts/check_features.py`

import joblib
import numpy as np

# Load the locally trained model
# Assuming the script is run from the repository root
model = joblib.load("inference_service/model.joblib")

# Check how many input features the model expects
print(f"✅ Model expects {model.n_features_in_} features")

# Optionally: Try predicting with random data
try:
    dummy = np.random.rand(1, model.n_features_in_)
    pred = model.predict(dummy)
    print(f"✅ Prediction succeeded with {model.n_features_in_} features: {pred}")
except Exception as e:
    print(f"❌ Prediction failed: {e}")

