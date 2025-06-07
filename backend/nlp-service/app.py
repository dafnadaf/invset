"""
consumer 'social_data' → NLP → producer 'text_features'
GET /health 200 OK
"""
import os, json
from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer

# TODO: plug in real sentiment and topic models

app = FastAPI()
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP,
                         value_serializer=lambda v: json.dumps(v).encode())
consumer = KafkaConsumer(
    "social_data",
    bootstrap_servers=BOOTSTRAP,
    value_deserializer=lambda m: json.loads(m.decode()),
    group_id="nlp",
)

@app.on_event("startup")
def start_loop():
    import threading
    threading.Thread(target=loop, daemon=True).start()

def loop():
    for msg in consumer:
        text = msg.value["text"]
        out = {**msg.value,
               "sentiment": {"neg":0.1,"neu":0.8,"pos":0.1},
               "topic": 0}
        producer.send("text_features", out)

@app.get("/health")
def health():
    return {"status":"ok"}
