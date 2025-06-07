"""
Задача: Периодически считывать CSV/Excel из папки /data
или по REST‑API и слать записи в Kafka topic 'financial_data'
"""
import os, time, json
import pandas as pd
from kafka import KafkaProducer

# TODO: replace with object storage watcher and proper schema

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP,
                         value_serializer=lambda v: json.dumps(v).encode())

def process_file(path: str) -> None:
    df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    for _, row in df.iterrows():
        msg = row.to_dict()
        producer.send("financial_data", msg)
    producer.flush()

if __name__ == "__main__":
    POLL = int(os.getenv("FIN_POLL_SEC", 3600))
    DATA_DIR = "/data"
    sent = set()
    while True:
        for f in os.listdir(DATA_DIR):
            abspath = os.path.join(DATA_DIR, f)
            if abspath not in sent:
                process_file(abspath)
                sent.add(abspath)
        time.sleep(POLL)
