# score.py

import json
import joblib
import numpy as np
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path("fraud_detection_rf_model")
    model = joblib.load(model_path)

def run(data):
    try:
        input_data = np.array(json.loads(data)["data"])
        prediction = model.predict(input_data)
        return json.dumps({"result": prediction.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})
