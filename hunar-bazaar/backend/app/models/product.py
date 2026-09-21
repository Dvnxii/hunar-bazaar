"""Product document shape."""
from datetime import datetime, timezone


def new_product_document(
    seller_id: str,
    title: str,
    description: str,
    price: float,
    category: str,
    stock: int,
    images: list[str],
    translations: dict | None = None,
) -> dict:
    return {
        "seller_id": seller_id,
        "title": title,
        "description": description,
        "price": price,
        "category": category,
        "stock": stock,
        "images": images,
        # per-locale overrides, e.g. {"hi": {"title": "...", "description": "..."}}
        "translations": translations or {},
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }
