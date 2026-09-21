"""Order document shape, including the encrypted-QR delivery handoff fields."""
from datetime import datetime, timezone
from typing import Literal

OrderStatus = Literal[
    "placed", "confirmed", "assigned", "out_for_delivery", "delivered", "cancelled"
]


def new_order_document(
    buyer_id: str,
    items: list[dict],   # [{product_id, quantity, price}]
    total_amount: float,
    shipping_address: dict,
) -> dict:
    return {
        "buyer_id": buyer_id,
        "items": items,
        "total_amount": total_amount,
        "shipping_address": shipping_address,
        "status": "placed",
        "delivery_agent_id": None,
        # Populated once an agent is assigned: AES-128 encrypted payload
        # (order id + delivery-agent id + expiry) rendered as a QR code and
        # decrypted at the doorstep for last-mile verification.
        "delivery_qr_payload_encrypted": None,
        "created_at": datetime.now(timezone.utc),
        "delivered_at": None,
    }
