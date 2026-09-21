"""Seller portal: manage own catalog, view incoming orders for own products."""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.db.mongodb import get_database
from app.models.product import new_product_document
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/api/seller", tags=["seller"])


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, user=Depends(require_roles("seller"))):
    db = get_database()
    doc = new_product_document(seller_id=user["id"], **payload.model_dump())
    result = await db.products.insert_one(doc)
    return ProductOut(id=str(result.inserted_id), **{k: doc[k] for k in ("seller_id", "title", "description", "price", "category", "stock", "images", "is_active")})


@router.get("/products", response_model=list[ProductOut])
async def my_products(user=Depends(require_roles("seller"))):
    db = get_database()
    cursor = db.products.find({"seller_id": user["id"]})
    return [
        ProductOut(id=str(p["_id"]), **{k: p[k] for k in ("seller_id", "title", "description", "price", "category", "stock", "images", "is_active")})
        async for p in cursor
    ]


@router.patch("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, payload: ProductUpdate, user=Depends(require_roles("seller"))):
    db = get_database()
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    result = await db.products.find_one_and_update(
        {"_id": ObjectId(product_id), "seller_id": user["id"]}, {"$set": updates}, return_document=True,
    )
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found or not owned by this seller")
    return ProductOut(id=str(result["_id"]), **{k: result[k] for k in ("seller_id", "title", "description", "price", "category", "stock", "images", "is_active")})


@router.get("/orders")
async def incoming_orders(user=Depends(require_roles("seller"))):
    db = get_database()
    product_ids = [str(p["_id"]) async for p in db.products.find({"seller_id": user["id"]}, {"_id": 1})]
    cursor = db.orders.find({"items.product_id": {"$in": product_ids}})
    return [{**o, "_id": str(o["_id"])} async for o in cursor]
