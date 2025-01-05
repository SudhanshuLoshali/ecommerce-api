"""
Pydantic models for request/response validation.
"""

from typing import List, Annotated

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """
    Base schema for Product with common attributes.
    """
    name: Annotated[str, Field(min_length=1)]
    description: Annotated[str, Field(min_length=1)]
    price: Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)]


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
    
    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    """
    Schema for items within an order creation request.
    """
    product_id: int
    quantity: Annotated[int, Field(gt=0)]


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
    
    model_config = ConfigDict(from_attributes=True)
