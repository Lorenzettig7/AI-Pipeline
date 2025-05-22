import xgboost as xgb
import numpy as np

# Load your trained model
booster = xgb.Booster()
booster.load_model("model.bst")

# Try various feature counts to determine compatibility
for i in range(60, 100):
    try:
        dmatrix = xgb.DMatrix(np.random.rand(1, i))
        booster.predict(dmatrix)
        print(f"✅ Model accepts {i} features")
    except:
        print(f"❌ Model rejects {i} features")

