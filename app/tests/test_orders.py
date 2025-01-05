"""
Test module for order-related API endpoints.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app
from app.models import Base
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_order(test_db):
    client = TestClient(app)
    
    # First create a product
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99, "stock": 10},
    )
    product_id = product_response.json()["id"]
    
    # Then create an order
    order_response = client.post(
        "/orders/",
        json={"products": [{"product_id": product_id, "quantity": 2}]},
    )
    assert order_response.status_code == 201
    data = order_response.json()
    assert data["status"] == "pending"
    assert data["total_price"] == 199.98

def test_create_order_insufficient_stock(test_db):
    client = TestClient(app)
    
    # Create a product with low stock
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99, "stock": 1},
    )
    product_id = product_response.json()["id"]
    
    # Try to order more than available stock
    order_response = client.post(
        "/orders/",
        json={"products": [{"product_id": product_id, "quantity": 2}]},
    )
    assert order_response.status_code == 400
