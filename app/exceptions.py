"""
Custom exception classes.
"""

from fastapi import HTTPException, status


class InsufficientStockException(HTTPException):
    """
    Exception raised when attempting to order more items than available in stock.
    """

    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for product with id {product_id}"
        )


class ProductNotFoundException(HTTPException):
    """
    Exception raised when attempting to access a non-existent product.
    """

    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
