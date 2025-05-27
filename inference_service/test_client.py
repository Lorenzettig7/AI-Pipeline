import requests
import pandas as pd

df = pd.read_csv("cleaned_ddos.csv")

# ✅ STRIP spaces from all column names
df.columns = df.columns.str.strip()

# Drop the label
X = df.drop(columns=["Label"])  # no leading space now
sample = X.iloc[0]
features = sample.tolist()

response = requests.post(
    "http://localhost:8000/predict",
    json={"features": features}
)

print("Status Code:", response.status_code)
print("Response:", response.json())

