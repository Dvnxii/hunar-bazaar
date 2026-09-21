# Hunar Bazaar—Multilingual E-Commerce Platform for Local Artisans

A role-based e-commerce platform with four portals (buyer, seller, delivery
agent, admin), built as: **React + Tailwind** frontend, **FastAPI**
backend, **MongoDB** for persistence, **Redis** for OTP/session state, a
**C++ (CMake)** AES-128 module for encrypted delivery QR codes, and a
**scikit-learn** content-based product recommender.

This is a project **scaffold**: every layer is wired end-to-end and runs,
but the business logic is intentionally minimal so you can extend it
feature-by-feature rather than untangle a finished app.

## Architecture

frontend/   React 18 + Vite + Tailwind. Four portals under src/portals/,
            role-gated by <ProtectedRoute>. i18n via react-i18next (en/hi
            seeded, add more under src/i18n/).
backend/    FastAPI. JWT auth delivered as HTTP-only cookies (never in
            localStorage), Google OAuth via Authlib, Redis-backed OTP.
            Routers split by portal: routers/{auth,buyer,seller,delivery,admin}.py
crypto/     Standalone CMake C++17 project. Textbook AES-128 (FIPS-197),
            CBC + PKCS#7, exposed as a `qr_crypto encrypt|decrypt` CLI that
            the backend shells out to (app/services/qr_service.py).
recommender/ scikit-learn TF-IDF + cosine-similarity recommender
            (model.py), trained offline (train.py) and loaded by the
            backend for "similar products" (routers/buyer.py).

## Why a subprocess for the crypto, not a Python AES lib?
The resume line this scaffold implements is specifically a **custom AES-128
system in C++**. Keeping the cipher in C++ behind a small CLI means the
same binary can later be reused outside the web stack (an embedded
scanner, a delivery-agent CLI tool) without re-implementing it, and keeps
the crypto surface auditable in one small, dependency-free module.

## Running it

**Everything via Docker:**
bash
docker compose up --build
# frontend -> http://localhost:4173
# backend  -> http://localhost:8000/api/health

**Locally, for faster iteration:**
```bash
# 1. crypto — build once, backend calls the resulting binary
cd crypto && cmake -B build && cmake --build build
mkdir -p ../backend/bin && cp build/qr_crypto ../backend/bin/

# 2. backend
cd ../backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in JWT_SECRET_KEY, Google OAuth creds, etc.
# make sure mongo + redis are running locally (or point MONGO_URI/REDIS_URL elsewhere)
uvicorn app.main:app --reload

# 3. frontend
cd ../frontend
npm install
npm run dev   # -> http://localhost:5173, proxies /api to :8000

Recommender (optional, buyer portal works without it via a
same-category fallback):
bash
cd recommender
pip install -r requirements.txt
python train.py --source mongo   # needs products already in Mongo

## What's stubbed vs. real

| Layer | Status |
| JWT auth (access + refresh cookies), password hashing | Real |
| Redis OTP generation/verification | Real (email delivery is a TODO — currently just expires silently) |
| Google OAuth | Real flow, needs your own `GOOGLE_CLIENT_ID`/`SECRET` in `.env` |
| AES-128 encryption (C++) | Real, FIPS-197 verified — see `crypto/` |
| Product CRUD, cart, orders, stock decrement | Real, minimal validation |
| Delivery QR generate/scan | Real crypto + status transition; QR **camera** scanning is a hex-paste stand-in (swap in `html5-qrcode` or similar) |
| scikit-learn recommender | Real TF-IDF pipeline, needs `train.py` run against real catalog data |
| Payments | Not implemented |
| Admin analytics beyond counts | Not implemented |
| Multilingual product translations | Data model supports per-locale overrides (`products.translations`); no admin UI to edit them yet |

## Next steps, roughly in priority order

1. Wire an actual email/SMS provider into `otp_service.py` instead of returning the code from `generate_and_store_otp` unused.
2. Add product image upload (S3/Cloudinary) — `images: []` is a placeholder today.
3. Swap the delivery QR scan page's textarea for a real camera scanner.
4. Add a seller payout / commission model if this becomes a real marketplace.
5. Write tests — none exist yet in this scaffold.
