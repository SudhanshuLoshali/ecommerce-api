"""
Pydantic models for request/response validation.
"""

from typing import List

from pydantic import BaseModel, constr, confloat, conint


class ProductBase(BaseModel):
    """
    Base schema for Product with common attributes.
    """
    name: constr(min_length=1)
    description: constr(min_length=1)
    price: confloat(gt=0)
    stock: conint(ge=0)


class ProductCreate(ProductBase):
    """
    Schema for creating a new product, inherits from ProductBase.
    """
    pass


class Product(ProductBase):
    """
    Schema for product responses.
    """
    id: int

    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    """
    Schema for items within an order creation request.
    """
    product_id: int
    quantity: conint(gt=0)


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    """
    products: List[OrderItemCreate]


class Order(BaseModel):
    """
    Schema for order responses.
    """
    id: int
    total_price: float
    status: str
    products: List[Product]

    class Config:
        orm_mode = True
