"""
User document shape as stored in MongoDB (not a pydantic schema for API I/O -
see schemas/ for that). One collection, discriminated by `role`.
"""
from datetime import datetime, timezone
from typing import Literal, Optional

ROLE = Literal["buyer", "seller", "delivery_agent", "admin"]


def new_user_document(
    name: str,
    email: str,
    hashed_password: Optional[str],
    role: ROLE,
    language: str = "en",
    oauth_provider: Optional[str] = None,
) -> dict:
    return {
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "language": language,          # preferred UI locale, drives the multilingual portal
        "oauth_provider": oauth_provider,
        "is_verified": False,          # flips true after OTP verification
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        # role-specific extras
        "seller_profile": {"store_name": None, "gst_number": None} if role == "seller" else None,
        "delivery_profile": {"vehicle_number": None, "zone": None} if role == "delivery_agent" else None,
    }
