"""
Main FastAPI application module.
"""

from typing import List

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app.models import Base, order_products, Product as ProductModel, Order as OrderModel
from app.schemas import Product as ProductSchema, ProductCreate, Order as OrderSchema, OrderCreate
from app.database import get_db, engine
from app.exceptions import ProductNotFoundException, InsufficientStockException

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")


@app.get("/products", response_model=List[ProductSchema])
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products from the database.
    """
    return db.query(ProductModel).all()


@app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the database.
    """
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post("/orders", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    total_price = 0
    order_items = []

    # First validate all products and calculate total price
    for item in order.products:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not product:
            raise ProductNotFoundException(item.product_id)

        if product.stock < item.quantity:
            raise InsufficientStockException(item.product_id)

        product.stock -= item.quantity
        total_price += product.price * item.quantity
        order_items.append({
            "product": product,
            "quantity": item.quantity
        })

    # Create the order
    db_order = OrderModel(
        total_price=total_price,
        status="pending"
    )
    
    db.add(db_order)
    db.flush()
    
    for item in order_items:
        db.execute(
            order_products.insert().values(
                order_id=db_order.id,
                product_id=item["product"].id,
                quantity=item["quantity"]
            )
        )

    db.commit()
    
    db.refresh(db_order)
    return db_order
