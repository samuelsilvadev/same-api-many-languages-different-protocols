import strawberry
from typing import List, Optional, NewType, cast
from datetime import datetime
from pydantic import BaseModel, EmailStr


@strawberry.type
class BaseUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


@strawberry.type
class CreateUserPayload(BaseUser):
    password: str


@strawberry.type
class CreateUserResponse(BaseUser):
    id: int


@strawberry.type
class GetUserResponse(BaseUser):
    id: int


class BaseProduct(BaseModel):
    name: str
    price: float
    amount: int

    class Config:
        orm_mode = True


class CreateProductPayload(BaseProduct):
    pass


class CreateProductResponse(BaseProduct):
    id: int


class ProductResponse(BaseProduct):
    id: int


class OrderProduct(BaseModel):
    product_id: int
    price: float


class BaseOrder(BaseModel):
    order_id: Optional[int] = None
    user_id: int
    products: List[OrderProduct]


class CreateOrderPayload(BaseOrder):
    pass


class NewOrder(BaseModel):
    id: int
    created_at: datetime


class CreateOrderAndProdcutsResponse(BaseModel):
    order: NewOrder
    products: List[OrderProduct]


class UpdateOrderPayload(BaseModel):
    order_id: int
    user_id: int
    products: List[OrderProduct]


class UpdatedOrder(BaseModel):
    id: int
    updated_at: datetime


class UpdatedOrderAndProductsResponse(BaseModel):
    order: UpdatedOrder
    products: List[OrderProduct]
