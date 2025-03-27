from src.config import logging_instance
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from src.db import get_session
from src.repository import products_repository
from src.routes.api_key_validator import validate_api_key
from .schemas import CreateProductPayload, CreateProductResponse


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product(
    product: CreateProductPayload,
    db=Depends(get_session),
    api_key=Security(APIKeyHeader(name="X-API-Key")),
):
    try:
        validate_api_key(api_key)

        new_product = products_repository.create_product(db, product)

        return CreateProductResponse(
            id=new_product.id,
            name=new_product.name,
            price=new_product.price,
            amount=new_product.amount,
        )
    except Exception as error:
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
