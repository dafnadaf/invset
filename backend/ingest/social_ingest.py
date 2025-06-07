"""
Поток твитов по ключевым словам и Telegram-сообщений.
Отправляет JSON → topic 'social_data'
"""

import os, json, asyncio
from datetime import datetime
from kafka import KafkaProducer
import tweepy
from telethon import TelegramClient, events

# TODO: handle rate limits and errors from APIs

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP,
                         value_serializer=lambda v: json.dumps(v).encode())

# ---------- Twitter ----------
tw_auth = tweepy.OAuth2AppHandler(
    os.getenv("TW_API_KEY"), os.getenv("TW_API_SECRET"))
client = tweepy.Client(bearer_token=os.getenv("TW_BEARER"))

KEYWORDS = ["Газпром", "Сбербанк", "Лукойл"]  # ← расширьте YAML-файлом

class TWStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        producer.send("social_data", {
            "source": "twitter",
            "text": tweet.text,
            "ts": tweet.created_at.isoformat()
        })

tw_stream = TWStream(bearer_token=os.getenv("TW_BEARER"))
# add rules once
tw_stream.add_rules([tweepy.StreamRule(k) for k in KEYWORDS])

# ---------- Telegram ----------
tg_api_id = os.getenv("TG_API_ID")
tg_api_hash = os.getenv("TG_API_HASH")
tg_client = TelegramClient("ingest", tg_api_id, tg_api_hash)

@tg_client.on(events.NewMessage(chats=os.getenv("TG_CHANNELS").split(",")))
async def handler(event):
    producer.send("social_data", {
        "source": "telegram",
        "text": event.raw_text,
        "ts": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    tg_client.start()
    asyncio.get_event_loop().create_task(tg_client.run_until_disconnected())
    tw_stream.filter(expansions=None)
