"""
JWT issuance/verification, password hashing, and role-based access-control
dependencies. Tokens are delivered as HTTP-only cookies (see routers/auth.py),
never read from localStorage on the frontend.
"""
from datetime import datetime, timedelta, timezone
from typing import Literal
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Role = Literal["buyer", "seller", "delivery_agent", "admin"]
ACCESS_COOKIE_NAME = "hb_access_token"
REFRESH_COOKIE_NAME = "hb_refresh_token"

def hash_password(raw: str)->str:
    return pwd_context.hash(raw)

def verify_password(raw: str, hashed: str)->bool:
    return pwd_context.verify(raw, hashed)

def _create_token(subject: str, role: str, expires_delta:timedelta,token_type:str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub":subject,
        "role":role,
        "type":token_type,
        "iat":now,
        "exp":now+expires_delta,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_access_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, timedelta(minutes=settings.access_token_expire_minutes), "access"
    )


def create_refresh_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, timedelta(days=settings.refresh_token_expire_days), "refresh"
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")


async def get_current_user(request: Request) -> dict:
    """Reads the access-token HTTP-only cookie and returns {id, role}."""
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong token type")
    return {"id": payload["sub"], "role": payload["role"]}


def require_roles(*allowed: Role):
    """Dependency factory: require_roles("seller", "admin") guards a route."""

    async def _checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient role for this action")
        return user

    return _checker
