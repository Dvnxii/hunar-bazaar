"""
Centralized settings, loaded from environment variables / .env.
Every other module reads config from here instead of touching os.environ directly.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Hunar Bazaar"
    env: str = "development"
    mongo_uri: str = "mongodb://mongo:27017"
    mongo_db_name: str = "hunar_bazaar"
    redis_url: str = "redis://redis:6379/0"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cookie_secure: bool = False
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/oauth/google/callback"
    otp_ttl_seconds: int = 300
    otp_length: int = 6
    qr_crypto_bin: str = "/app/bin/qr_crypto"
    aes_qr_key_hex: str = "000102030405060708090a0b0c0d0e0f"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
settings = Settings()
