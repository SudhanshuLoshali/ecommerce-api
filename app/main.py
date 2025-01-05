"""
Main FastAPI application module.
"""

from typing import List

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db, engine
import exceptions

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")


@app.get("/products", response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products from the database.

    Args:
        db (Session): Database session dependency

    Returns:
        List[Product]: List of all products in the database
    """
    return db.query(models.Product).all()


@app.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the database.

    Args:
        product (ProductCreate): Product data to create
        db (Session): Database session dependency

    Returns:
        Product: Created product data
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post("/orders", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order and update product stock levels.

    Args:
        order (OrderCreate): Order data including products and quantities
        db (Session): Database session dependency

    Returns:
        Order: Created order data

    Raises:
        ProductNotFoundException: If a product in the order doesn't exist
        InsufficientStockException: If there's not enough stock for any product
    """
    total_price = 0
    order_products = []

    for item in order.products:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise exceptions.ProductNotFoundException(item.product_id)

        if product.stock < item.quantity:
            raise exceptions.InsufficientStockException(item.product_id)

        product.stock -= item.quantity
        total_price += product.price * item.quantity
        order_products.append(product)

    db_order = models.Order(
        total_price=total_price,
        status="pending",
        products=order_products
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
