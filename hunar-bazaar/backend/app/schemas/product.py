from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float = Field(gt=0)
    category: str
    stock: int = Field(ge=0)
    images: list[str] = []
    translations: dict = {}


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    images: Optional[list[str]] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str
    price: float
    category: str
    stock: int
    images: list[str]
    is_active: bool
