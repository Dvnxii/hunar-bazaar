# Hunar Bazaar — Multilingual E-Commerce Platform

Hunar Bazaar is a role-based e-commerce platform designed for local artisans. It has separate portals for buyers, sellers, delivery agents, and administrators.

The project uses React and Tailwind CSS on the frontend, FastAPI on the backend, MongoDB for storing application data, and Redis for OTP/session-related data.

It also includes a custom AES-128 implementation in C++ for securing delivery QR codes and a product recommendation system built using scikit-learn.

## Main Features

- Buyer, seller, delivery agent, and admin portals
- JWT-based authentication using HTTP-only cookies
- Google login using OAuth
- OTP handling with Redis
- Product and order management
- Shopping cart and stock management
- Delivery QR code generation and verification
- Custom AES-128 encryption written in C++
- Product recommendations using TF-IDF and cosine similarity
- English and Hindi language support
- Docker setup for running the complete application

## Project Structure

```text
hunar-bazaar/
│
├── frontend/
│   ├── src/
│   │   ├── portals/
│   │   └── i18n/
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── buyer.py
│   │   │   ├── seller.py
│   │   │   ├── delivery.py
│   │   │   └── admin.py
│   │   └── services/
│   └── ...
│
├── crypto/
│   └── ...
│
├── recommender/
│   ├── model.py
│   └── train.py
│
└── docker-compose.yml
```

## Tech Stack

| Part | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | FastAPI, Python |
| Database | MongoDB |
| Session/OTP Storage | Redis |
| Authentication | JWT, Google OAuth |
| Encryption | C++17, AES-128, CMake |
| Recommendation System | scikit-learn |
| Deployment | Docker |

## Application Structure

There are four main portals in the application:

### Buyer

Buyers can browse products, add products to their cart, place orders, and receive product recommendations.

### Seller

The seller portal is used for managing products, stock, and orders.

### Delivery Agent

The delivery portal handles delivery-related operations and QR verification.

### Admin

The admin portal provides access to administrative operations and basic application statistics.

Access to the different portals is controlled using protected routes based on the user's role.

## Authentication

The backend uses JWT authentication with HTTP-only cookies.

The tokens are not stored in `localStorage`, which avoids exposing them directly to client-side JavaScript.

Google OAuth is also supported through Authlib.

To use Google login, the required credentials need to be added to the backend `.env` file.

## OTP Handling

Redis is used for storing OTP and session-related information.

The current OTP flow handles generation, storage, verification, and expiration.

Email delivery is not connected yet, so an actual email/SMS provider needs to be added for production use.

## Delivery QR Codes

The project includes a separate C++ module for AES-128 encryption.

The crypto module is a standalone CMake/C++17 project:

```text
crypto/
```

It provides a command-line program:

```text
qr_crypto encrypt
qr_crypto decrypt
```

The FastAPI backend calls this program when generating or verifying delivery QR data.

The encryption implementation uses:

```text
AES-128
CBC mode
PKCS#7 padding
```

The implementation follows the AES specification described in FIPS-197.

Keeping the encryption code in a separate C++ module also makes it possible to reuse the same binary in another application later, such as a delivery-agent utility or scanner.

## Product Recommendations

The buyer portal includes a basic content-based recommendation system.

The recommender uses:

```text
Product information
      ↓
TF-IDF
      ↓
Cosine similarity
      ↓
Similar products
```

The model is implemented using scikit-learn.

It can be trained using the product catalog from MongoDB:

```bash
cd recommender
pip install -r requirements.txt
python train.py --source mongo
```

The recommendation system is optional. If it is not available, the buyer portal falls back to showing products from the same category.

## Multilingual Support

The frontend uses `react-i18next` for language support.

English and Hindi are included initially:

```text
src/i18n/
```

Additional languages can be added by creating the corresponding translation files.

The product data model also supports translated product information through:

```text
products.translations
```

The admin interface for editing these translations has not been implemented yet.

## Running the Project

### Using Docker

The easiest way to run the complete application is:

```bash
docker compose up --build
```

After the containers start:

```text
Frontend → http://localhost:4173
Backend  → http://localhost:8000/api/health
```

### Running Locally

If you want to work on the project without rebuilding Docker containers every time, the services can also be started separately.

### 1. Build the Crypto Module

```bash
cd crypto

cmake -B build
cmake --build build

mkdir -p ../backend/bin
cp build/qr_crypto ../backend/bin/
```

### 2. Start the Backend

```bash
cd ../backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Add the required values such as:

```env
JWT_SECRET_KEY=your_secret
MONGO_URI=your_mongodb_connection
REDIS_URL=your_redis_connection

GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

Make sure MongoDB and Redis are running locally, or point the application to remote instances.

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend runs on:

```text
http://localhost:8000
```

### 3. Start the Frontend

```bash
cd ../frontend

npm install
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

The development server proxies `/api` requests to the backend.

## What Is Implemented?

The project currently has the following status:

| Feature | Status |
|---|---|
| JWT authentication | Implemented |
| Password hashing | Implemented |
| Redis OTP handling | Implemented |
| Google OAuth | Implemented |
| AES-128 encryption | Implemented |
| Product CRUD | Implemented |
| Cart | Implemented |
| Orders | Implemented |
| Stock updates | Implemented |
| Delivery QR generation | Implemented |
| Delivery QR verification | Implemented |
| Product recommender | Implemented |
| English/Hindi UI | Implemented |
| Payments | Not implemented |
| Advanced admin analytics | Not implemented |
| Product translation management UI | Not implemented |
| Real camera QR scanning | Not implemented |
| Email/SMS OTP delivery | Not implemented |

The QR scanning page currently uses a hex-paste input instead of accessing the device camera. A library such as `html5-qrcode` can be integrated later.

## Future Improvements

Some of the next things that can be added are:

1. Connect an email or SMS service for OTP delivery.
2. Add product image uploads using S3, Cloudinary, or another storage service.
3. Replace the QR hex-paste field with a camera-based scanner.
4. Add seller commissions and payout handling.
5. Add payment gateway integration.
6. Add more languages and an admin interface for product translations.
7. Add automated tests for the backend and frontend.
8. Improve admin analytics and reporting.

## License

MIT
