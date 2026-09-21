"""
Google OAuth login. Uses Authlib's async OAuth client; the frontend redirects
the browser to /api/auth/oauth/google/login and Google redirects back to the
callback route, which issues our own JWT cookies exactly like password login.
"""
from authlib.integrations.starlette_client import OAuth

from app.core.config import settings

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
