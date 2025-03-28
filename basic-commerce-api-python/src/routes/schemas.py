from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserPayload(BaseUser):
    password: str


class CreateUserResponse(BaseUser):
    id: int


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
