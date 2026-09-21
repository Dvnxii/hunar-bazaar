FROM python:3.12-slim AS backend

WORKDIR /app

# Build the C++ AES-128 QR-crypto binary used by app/services/qr_service.py
FROM gcc:13 AS crypto-build
WORKDIR /crypto
COPY crypto/ .
RUN apt-get update && apt-get install -y cmake && \
    cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build

FROM backend AS final
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY --from=crypto-build /crypto/build/qr_crypto /app/bin/qr_crypto
RUN chmod +x /app/bin/qr_crypto

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
