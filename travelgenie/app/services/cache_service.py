import redis
import json
from app.core.config import settings


try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2
    )

    # Test connection once at startup
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("Redis connected successfully.")

except Exception as e:
    print("Redis not available. Running without cache.")
    REDIS_AVAILABLE = False
    redis_client = None


def get_cache(key: str):
    if not REDIS_AVAILABLE:
        return None

    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    except Exception as e:
        print("Redis GET failed:", e)
        return None


def set_cache(key: str, value, expiry: int = 3600):
    if not REDIS_AVAILABLE:
        return

    try:
        redis_client.setex(
            key,
            expiry,
            json.dumps(value)
        )
    except Exception as e:
        print("Redis SET failed:", e)