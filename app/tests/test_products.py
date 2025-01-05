"""
Test module for product-related API endpoints.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    """
    Creates tables before each test and drops them after.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_product(test_db):
    """
    Test product creation endpoint.

    Verifies:
        - Successful product creation
        - Correct response status code
        - Response data matches input data
    """
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
    """
    Test product retrieval endpoint.

    Verifies:
        - Successful retrieval of products
        - Correct response status code
        - Response contains a list
    """
    client = TestClient(app)
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
