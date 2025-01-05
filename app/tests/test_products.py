"""
Test module for product-related API endpoints.
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
    """
    Fixture to create a test database for each test.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_product(test_db):
    client = TestClient(app)
    response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99, "stock": 10},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    assert data["stock"] == 10

def test_get_products(test_db):
    client = TestClient(app)
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
