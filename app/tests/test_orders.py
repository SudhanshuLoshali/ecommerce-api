"""
Test module for order-related API endpoints.
"""

from fastapi.testclient import TestClient
from main import app


def test_create_order():
    """
    Test order creation with valid data.

    Verifies:
        - Successful order creation
        - Correct calculation of total price
        - Proper order status
    """
    client = TestClient(app)

    # create a product
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99, "stock": 10},
    )
    product_id = product_response.json()["id"]

    # create an order
    order_response = client.post(
        "/orders/",
        json={"products": [{"product_id": product_id, "quantity": 2}]},
    )
    assert order_response.status_code == 201
    data = order_response.json()
    assert data["status"] == "pending"
    assert data["total_price"] == 199.98


def test_create_order_insufficient_stock():
    """
    Test order creation with insufficient stock.

    Verifies:
        - Proper error handling for insufficient stock
        - Correct error status code
    """
    client = TestClient(app)

    # Create a product with low stock
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99, "stock": 1},
    )
    product_id = product_response.json()["id"]

    # order more than available stock
    order_response = client.post(
        "/orders/",
        json={"products": [{"product_id": product_id, "quantity": 2}]},
    )
    assert order_response.status_code == 400
