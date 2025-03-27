from sqlalchemy.orm import Session
from src.config import logging_instance
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from src.db import get_session
from src.repository import products_repository
from src.routes.api_key_validator import validate_api_key
from .schemas import CreateProductPayload, CreateProductResponse, ProductResponse


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product(
    product: CreateProductPayload,
    db: Session = Depends(get_session),
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


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_session)):
    try:
        product = products_repository.get_product_by_id(db, id)

        if product is None:
            logging_instance.info(f"Product with {id} does not exist")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            amount=product.amount,
        )
    except Exception as error:
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/")
def get_all_products(db: Session = Depends(get_session)):
    try:
        products = products_repository.get_all_products(db)

        return [ProductResponse(**product.__dict__) for product in products]
    except Exception as error:
        logging_instance.error(error)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
