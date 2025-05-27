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

