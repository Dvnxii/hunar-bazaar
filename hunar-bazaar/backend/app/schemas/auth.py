from typing import Literal, Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["buyer", "seller", "delivery_agent"]  # admin accounts are provisioned manually
    language: str = "en"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class OtpRequest(BaseModel):
    email: EmailStr


class OtpVerifyRequest(BaseModel):
    email: EmailStr
    code: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    language: str
    is_verified: bool


class TokenResponse(BaseModel):
    user: UserOut
    message: str = "Logged in"
