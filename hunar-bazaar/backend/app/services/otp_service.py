"""
Redis-backed OTP verification. Codes are stored with a TTL so they
self-expire; no OTP is ever persisted in Mongo or logged.
"""
import random
import string

from app.core.config import settings
from app.redis_client import redis_client

OTP_KEY_PREFIX = "otp:"


def _key(email: str) -> str:
    return f"{OTP_KEY_PREFIX}{email.lower()}"


async def generate_and_store_otp(email: str) -> str:
    code = "".join(random.choices(string.digits, k=settings.otp_length))
    await redis_client.set(_key(email), code, ex=settings.otp_ttl_seconds)
    # In production this hands off to an email/SMS provider instead of returning the code.
    return code


async def verify_otp(email: str, code: str) -> bool:
    stored = await redis_client.get(_key(email))
    if stored is None:
        return False
    if stored == code:
        await redis_client.delete(_key(email))
        return True
    return False
