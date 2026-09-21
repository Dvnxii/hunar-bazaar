"""
Registration, password login, OTP email verification, Google OAuth, and
logout. Access/refresh tokens are set as HTTP-only, SameSite=Lax cookies -
the frontend never touches the raw JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from bson import ObjectId

from app.core.config import settings
from app.core.security import (
    ACCESS_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.db.mongodb import get_database
from app.models.user import new_user_document
from app.schemas.auth import (
    LoginRequest,
    OtpRequest,
    OtpVerifyRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)
from app.services.oauth_service import oauth
from app.services.otp_service import generate_and_store_otp, verify_otp

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_auth_cookies(response: Response, user_id: str, role: str) -> None:
    access = create_access_token(user_id, role)
    refresh = create_refresh_token(user_id, role)
    common = dict(httponly=True, secure=settings.cookie_secure, samesite="lax")
    response.set_cookie(ACCESS_COOKIE_NAME, access, max_age=settings.access_token_expire_minutes * 60, **common)
    response.set_cookie(REFRESH_COOKIE_NAME, refresh, max_age=settings.refresh_token_expire_days * 86400, **common)


def _user_out(doc: dict) -> UserOut:
    return UserOut(
        id=str(doc["_id"]), name=doc["name"], email=doc["email"],
        role=doc["role"], language=doc.get("language", "en"), is_verified=doc.get("is_verified", False),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    db = get_database()
    if await db.users.find_one({"email": payload.email}):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    doc = new_user_document(
        name=payload.name, email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role, language=payload.language,
    )
    result = await db.users.insert_one(doc)
    await generate_and_store_otp(payload.email)  # triggers verification flow
    return {"id": str(result.inserted_id), "message": "Registered. Check your email for an OTP."}


@router.post("/otp/request")
async def request_otp(payload: OtpRequest):
    db = get_database()
    if not await db.users.find_one({"email": payload.email}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No account with that email")
    await generate_and_store_otp(payload.email)
    return {"message": "OTP sent"}


@router.post("/otp/verify")
async def confirm_otp(payload: OtpVerifyRequest, response: Response):
    if not await verify_otp(payload.email, payload.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired OTP")

    db = get_database()
    user = await db.users.find_one_and_update(
        {"email": payload.email}, {"$set": {"is_verified": True}}, return_document=True
    )
    _set_auth_cookies(response, str(user["_id"]), user["role"])
    return TokenResponse(user=_user_out(user))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response):
    db = get_database()
    user = await db.users.find_one({"email": payload.email})
    if not user or not user.get("hashed_password") or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
    if not user.get("is_verified"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account not verified - complete OTP verification")

    _set_auth_cookies(response, str(user["_id"]), user["role"])
    return TokenResponse(user=_user_out(user))


@router.get("/oauth/google/login")
async def google_login(request: Request):
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/oauth/google/callback")
async def google_callback(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo") or {}
    email = userinfo.get("email")
    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Google account has no email")

    db = get_database()
    user = await db.users.find_one({"email": email})
    if not user:
        doc = new_user_document(
            name=userinfo.get("name", email), email=email, hashed_password=None,
            role="buyer", oauth_provider="google",
        )
        doc["is_verified"] = True  # Google already verified the email
        result = await db.users.insert_one(doc)
        user = {**doc, "_id": result.inserted_id}

    _set_auth_cookies(response, str(user["_id"]), user["role"])
    return TokenResponse(user=_user_out(user))


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(ACCESS_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)
    return {"message": "Logged out"}


@router.get("/me", response_model=UserOut)
async def me(current=Depends(get_current_user)):
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(current["id"])})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return _user_out(user)
