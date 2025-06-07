from datetime import datetime, timedelta
import jwt, os, bcrypt, psycopg2

SECRET = os.getenv("JWT_SECRET", "topsecret")

def create_token(user_id, role):
    payload = {"uid": user_id, "role": role,
               "exp": datetime.utcnow() + timedelta(hours=12)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])

def hash_pw(pw: str):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def check_pw(pw: str, hashed):
    return bcrypt.checkpw(pw.encode(), hashed)
