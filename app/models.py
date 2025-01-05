"""
SQLAlchemy models for the e-commerce platform.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer)
)


class Product(Base):
    """
    Product model representing items available.

    Attributes:
        id (int): Unique identifier for the product
        name (str): Name of the product
        description (str): Detailed description of the product
        price (float): Price of the product
        stock (int): Current available quantity in stock
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)


class Order(Base):
    """
    Order model representing customer orders.

    Attributes:
        id (int): Unique identifier for the order
        total_price (float): Total price of all products in the order
        status (str): Current status of the order (pending/completed)
        products (relationship): Relationship to products through order_products table
    """

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    status = Column(String)
    products = relationship("Product", secondary=order_products, lazy="joined")
