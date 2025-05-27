import joblib
import numpy as np

# Load the locally trained model
model = joblib.load("model.joblib")

# Check how many input features the model expects
print(f"✅ Model expects {model.n_features_in_} features")

# Optionally: Try predicting with random data
try:
    dummy = np.random.rand(1, model.n_features_in_)
    pred = model.predict(dummy)
    print(f"✅ Prediction succeeded with {model.n_features_in_} features: {pred}")
except Exception as e:
    print(f"❌ Prediction failed: {e}")

