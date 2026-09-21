from typing import Literal, Optional
from pydantic import BaseModel


class OrderItemIn(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    shipping_address: dict


class OrderStatusUpdate(BaseModel):
    status: Literal["confirmed", "assigned", "out_for_delivery", "delivered", "cancelled"]
    delivery_agent_id: Optional[str] = None


class OrderOut(BaseModel):
    id: str
    buyer_id: str
    items: list[dict]
    total_amount: float
    status: str
    delivery_agent_id: Optional[str] = None
