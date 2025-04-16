import redis
import json
from app.core.config import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

def save_otp_registration(email: str, username: str, hashed_password: str, otp: str, ttl_seconds=600):
    data = {
        "username": username,
        "hashed_password": hashed_password,
        "otp": otp,
    }
    r.set(f"otp_reg:{email}", json.dumps(data), ex=ttl_seconds)

def get_otp_registration(email: str):
    data = r.get(f"otp_reg:{email}")
    return json.loads(data) if data else None

def delete_otp_registration(email: str):
    r.delete(f"otp_reg:{email}")
