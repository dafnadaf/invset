from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np, joblib, torch
from shap import TreeExplainer

# TODO: load models from persistent storage

class InVector(BaseModel):
    features: list[float]

rf = joblib.load("rf.pkl")
dnn_state = torch.load("dnn.pt", map_location="cpu")
dnn_dim = rf.n_features_in_

class Net(torch.nn.Module):
    def __init__(self, d):
        super().__init__()
        self.net = torch.nn.Identity()  # placeholder
    def forward(self, x):
        return self.net(x)

Net.forward = lambda self, x: x  # placeholder override

dnn = Net(dnn_dim)
dnn.load_state_dict(dnn_state)
dnn.eval()

explainer = TreeExplainer(rf)

app = FastAPI()

@app.post("/predict")
def predict(vec: InVector):
    x = np.array(vec.features).reshape(1, -1)
    rf_pred = rf.predict(x)[0]
    with torch.no_grad():
        dnn_pred = float(dnn(torch.tensor(x).float()))
    score = 0.6 * dnn_pred + 0.4 * rf_pred
    return {"rf": rf_pred, "dnn": dnn_pred, "score": score}

@app.post("/shap")
def shap_values(vec: InVector):
    x = np.array(vec.features).reshape(1, -1)
    # TODO: optimize SHAP calculation
    vals = explainer.shap_values(x)
    return {"shap": vals.tolist()}

@app.get("/health")
def health():
    return {"status": "ok"}
