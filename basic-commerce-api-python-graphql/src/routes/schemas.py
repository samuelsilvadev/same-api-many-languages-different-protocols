import strawberry
from typing import List, Optional
from datetime import datetime


@strawberry.type
class BaseUser:
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


@strawberry.type
class BaseProduct:
    name: str
    price: float
    amount: int

    class Config:
        orm_mode = True


@strawberry.type
class CreateProductPayload(BaseProduct):
    pass


@strawberry.type
class CreateProductResponse(BaseProduct):
    id: int


@strawberry.type
class ProductResponse(BaseProduct):
    id: int


@strawberry.type
class OrderProduct:
    product_id: int
    price: float


@strawberry.type
class BaseOrder:
    order_id: Optional[int] = None
    user_id: int
    products: List[OrderProduct]


@strawberry.type
class CreateOrderPayload(BaseOrder):
    pass


@strawberry.type
class NewOrder:
    id: int
    created_at: datetime


@strawberry.type
class CreateOrderAndProdcutsResponse:
    order: NewOrder
    products: List[OrderProduct]


@strawberry.type
class UpdateOrderPayload:
    order_id: int
    user_id: int
    products: List[OrderProduct]


@strawberry.type
class UpdatedOrder:
    id: int
    updated_at: datetime


@strawberry.type
class UpdatedOrderAndProductsResponse:
    order: UpdatedOrder
    products: List[OrderProduct]
