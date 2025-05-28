# This script sends a dummy POST request to the locally running inference service's
# /predict endpoint. It generates a random list of 78 features.
#
# Usage:
# 1. Ensure the inference service is running (e.g., via `docker-compose up`).
# 2. Run this script from the repository root: `python scripts/train_local.py`

import requests
import numpy as np

# Create a dummy input with 78 features
features = list(np.random.rand(78))

# Send POST request
response = requests.post(
    "http://localhost:8000/predict",
    json={"features": features}
)

print("Status Code:", response.status_code)
print("Response:", response.json())

