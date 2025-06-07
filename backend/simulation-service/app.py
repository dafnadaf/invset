import numpy as np
from fastapi import FastAPI
import requests, os
from pydantic import BaseModel

# TODO: integrate with real ML service

MODEL_EP = os.getenv("MODEL_EP", "http://model-service:8001/predict")
app = FastAPI()

class Scenario(BaseModel):
    base: list[float]
    idx: int
    delta: float
    iters: int = 5000

@app.post("/what-if")
def what_if(sc: Scenario):
    vec = sc.base[:]
    vec[sc.idx] += sc.delta
    return requests.post(MODEL_EP, json={"features": vec}).json()

@app.post("/monte-carlo")
def monte(sc: Scenario):
    base = np.array(sc.base)
    results = []
    for _ in range(sc.iters):
        noise = np.random.normal(0, 0.05, size=len(base))
        sample = (base * (1 + noise)).tolist()
        res = requests.post(MODEL_EP, json={"features": sample}).json()
        results.append(res["score"])
    return {"mean": float(np.mean(results)),
            "std": float(np.std(results)),
            "p95": float(np.percentile(results, 95))}

@app.get("/health")
def health():
    return {"status": "ok"}
