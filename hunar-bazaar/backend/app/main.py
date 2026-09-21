"""
FastAPI entrypoint. Wires up Mongo lifespan, CORS (credentialed, for the
HTTP-only cookie flow), session middleware (needed by Authlib's OAuth state),
and mounts every portal's router.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.routers import admin, auth, buyer, delivery, seller


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret_key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server; add prod origin at deploy time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(buyer.router)
app.include_router(seller.router)
app.include_router(delivery.router)
app.include_router(admin.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
