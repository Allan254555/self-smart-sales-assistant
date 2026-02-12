from __future__ import annotations
import redis
from backend.app.core.config import settings

def get_redis_client() -> redis.Redis:
    # decode_responses=True -> returns str not bytes
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
