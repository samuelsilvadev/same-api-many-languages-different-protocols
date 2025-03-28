from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.db import get_session
from src.routes.api_key_validator import validate_api_key
from src.config import logging_instance
from src.routes.schemas import (
    CreateOrderPayload,
    CreateOrderAndProdcutsResponse,
    NewOrder,
    OrderProduct,
)
from src.repository import users_repository, orders_repository

router = APIRouter(prefix="/orders", tags=["Orders"])


def _validate_user(db, user_id):
    if user_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="user_id is mandatory."
        )
    else:
        user = users_repository.get_user_by_id(db, user_id)

        if user is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid user.")


@router.post("/")
def create_order(
    order: CreateOrderPayload,
    db=Depends(get_session),
    api_key=Security(APIKeyHeader(name="X-API-Key")),
):
    try:
        validate_api_key(api_key)
        _validate_user(db, order.user_id)

        if order.order_id is not None:
            raise HTTPException(
                status_code=405,
                detail="You trying to update an order, to do that use the PUT verb.",
            )

        new_order, products = orders_repository.create_order_with_products(db, order)

        return CreateOrderAndProdcutsResponse(
            order=NewOrder(id=new_order.id, created_at=new_order.created_at),
            products=[
                OrderProduct(product_id=product.id, price=product.price)
                for product in products
            ],
        )
    except Exception as error:
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/")
def get_all_orders(
    user_id: int,
    db=Depends(get_session),
    api_key=Security(APIKeyHeader(name="X-API-Key")),
):
    try:
        validate_api_key(api_key)
        orders = orders_repository.get_all_orders_by_user(db, user_id)

        return orders
    except Exception as error:
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/{id}")
def get_order_by_id(
    order_id: int,
    db=Depends(get_session),
    api_key=Security(APIKeyHeader(name="X-API-Key")),
):
    try:
        validate_api_key(api_key)
        order = orders_repository.get_order_by_id(db, order_id)

        if order is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)

        return order
    except Exception as error:
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
