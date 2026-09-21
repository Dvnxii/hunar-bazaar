"""Buyer portal: browse products, place orders, track deliveries."""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user, require_roles
from app.db.mongodb import get_database
from app.models.order import new_order_document
from app.schemas.order import OrderCreate, OrderOut
from app.schemas.product import ProductOut
from app.services.recommend_service import recommend_similar_products

router = APIRouter(prefix="/api/buyer", tags=["buyer"])


@router.get("/products", response_model=list[ProductOut])
async def list_products(category: str | None = None):
    db = get_database()
    query = {"is_active": True}
    if category:
        query["category"] = category
    cursor = db.products.find(query)
    return [
        ProductOut(id=str(p["_id"]), **{k: p[k] for k in ("seller_id", "title", "description", "price", "category", "stock", "images", "is_active")})
        async for p in cursor
    ]


@router.get("/products/{product_id}/similar", response_model=list[str])
async def similar_products(product_id: str):
    db = get_database()
    catalog = [{"id": str(p["_id"]), "category": p["category"]} async for p in db.products.find({"is_active": True})]
    return recommend_similar_products(product_id, catalog)


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate, user=Depends(require_roles("buyer"))):
    db = get_database()
    items, total = [], 0.0
    for item in payload.items:
        product = await db.products.find_one({"_id": ObjectId(item.product_id), "is_active": True})
        if not product or product["stock"] < item.quantity:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Product {item.product_id} unavailable at that quantity")
        line_total = product["price"] * item.quantity
        items.append({"product_id": item.product_id, "quantity": item.quantity, "price": product["price"]})
        total += line_total

    doc = new_order_document(user["id"], items, total, payload.shipping_address)
    result = await db.orders.insert_one(doc)
    for item in payload.items:
        await db.products.update_one({"_id": ObjectId(item.product_id)}, {"$inc": {"stock": -item.quantity}})

    return OrderOut(id=str(result.inserted_id), buyer_id=user["id"], items=items, total_amount=total, status="placed")


@router.get("/orders", response_model=list[OrderOut])
async def my_orders(user=Depends(require_roles("buyer"))):
    db = get_database()
    cursor = db.orders.find({"buyer_id": user["id"]})
    return [
        OrderOut(id=str(o["_id"]), buyer_id=o["buyer_id"], items=o["items"], total_amount=o["total_amount"],
                 status=o["status"], delivery_agent_id=o.get("delivery_agent_id"))
        async for o in cursor
    ]
