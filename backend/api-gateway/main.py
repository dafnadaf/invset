from fastapi import FastAPI, Depends, HTTPException, Header
from auth import verify_token, create_token, check_pw
import psycopg2, os, redis, json, requests

# TODO: use async DB driver and proper connection pooling

app = FastAPI()
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
rdb = redis.Redis(host=REDIS_HOST, port=int(os.getenv("REDIS_PORT", "6379")))
PG_DSN = os.getenv("PG_DSN", "dbname=invest user=invest password=invest host=postgres")
MODEL_URL = os.getenv("MODEL_URL", "http://model-service:8001")

def require_auth(token: str = Header(...)):
    try:
        return verify_token(token)
    except Exception:
        raise HTTPException(401, "bad token")

@app.post("/login")
def login(user: str, pwd: str):
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    # TODO: user table schema will evolve
    cur.execute("select id,pwd_hash,role from users where login=%s", (user,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "no user")
    if not check_pw(pwd, row[1].encode()):
        raise HTTPException(401, "bad pw")
    return {"token": create_token(row[0], row[2])}

@app.get("/companies")
def companies(auth=Depends(require_auth)):
    cached = rdb.get("companies")
    if cached:
        return json.loads(cached)
    # TODO: replace with proper service discovery
    res = requests.get(f"{MODEL_URL}/latest").json()
    rdb.setex("companies", 5, json.dumps(res))
    return res

@app.get("/health")
def health():
    return {"status": "ok"}
