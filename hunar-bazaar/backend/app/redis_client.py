"""
Async Redis client, used for OTP storage and short-lived session/rate-limit keys.
"""
import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)
