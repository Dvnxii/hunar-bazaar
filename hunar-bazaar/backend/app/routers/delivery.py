"""
Delivery-agent portal: view assigned orders, generate the encrypted QR at
dispatch, and decrypt it at the doorstep to confirm handoff.
"""
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.security import require_roles
from app.db.mongodb import get_database
from app.services.qr_service import decrypt_delivery_payload, encrypt_delivery_payload

router = APIRouter(prefix="/api/delivery", tags=["delivery"])


class ScanRequest(BaseModel):
    ciphertext_hex: str


@router.get("/orders")
async def assigned_orders(user=Depends(require_roles("delivery_agent"))):
    db = get_database()
    cursor = db.orders.find({"delivery_agent_id": user["id"], "status": {"$ne": "delivered"}})
    return [{**o, "_id": str(o["_id"])} async for o in cursor]


@router.post("/orders/{order_id}/generate-qr")
async def generate_qr(order_id: str, user=Depends(require_roles("delivery_agent", "admin"))):
    db = get_database()
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")

    expiry = int((datetime.now(timezone.utc) + timedelta(hours=6)).timestamp())
    ciphertext_hex = await encrypt_delivery_payload(order_id, order["delivery_agent_id"], expiry)
    await db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {
        "delivery_qr_payload_encrypted": ciphertext_hex, "status": "out_for_delivery",
    }})
    # Frontend renders this hex string into a QR code image client-side.
    return {"ciphertext_hex": ciphertext_hex, "expires_at": expiry}


@router.post("/orders/scan")
async def scan_qr(payload: ScanRequest, user=Depends(require_roles("delivery_agent", "buyer", "admin"))):
    """Scanned at the doorstep - decrypts and, if valid/unexpired, marks the order delivered."""
    decrypted = await decrypt_delivery_payload(payload.ciphertext_hex)
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if decrypted["exp"] < now_ts:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "QR code expired")

    db = get_database()
    await db.orders.update_one(
        {"_id": ObjectId(decrypted["order_id"])},
        {"$set": {"status": "delivered", "delivered_at": datetime.now(timezone.utc)}},
    )
    return {"order_id": decrypted["order_id"], "status": "delivered"}
