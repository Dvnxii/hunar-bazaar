"""Admin portal: platform-wide oversight - users, orders, agent assignment."""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.db.mongodb import get_database
from app.schemas.order import OrderStatusUpdate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users")
async def list_users(user=Depends(require_roles("admin"))):
    db = get_database()
    cursor = db.users.find({}, {"hashed_password": 0})
    return [{**u, "_id": str(u["_id"])} async for u in cursor]


@router.patch("/users/{user_id}/deactivate")
async def deactivate_user(user_id: str, user=Depends(require_roles("admin"))):
    db = get_database()
    result = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"is_active": False}})
    if result.matched_count == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return {"message": "User deactivated"}


@router.get("/orders")
async def all_orders(user=Depends(require_roles("admin"))):
    db = get_database()
    cursor = db.orders.find({})
    return [{**o, "_id": str(o["_id"])} async for o in cursor]


@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, payload: OrderStatusUpdate, user=Depends(require_roles("admin"))):
    db = get_database()
    updates = {"status": payload.status}
    if payload.delivery_agent_id:
        updates["delivery_agent_id"] = payload.delivery_agent_id
    result = await db.orders.find_one_and_update({"_id": ObjectId(order_id)}, {"$set": updates}, return_document=True)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return {**result, "_id": str(result["_id"])}
