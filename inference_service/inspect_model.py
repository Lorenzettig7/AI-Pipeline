import joblib

model = joblib.load("model.joblib")
print("Expected feature names by model:")
print(model.get_booster().feature_names)

