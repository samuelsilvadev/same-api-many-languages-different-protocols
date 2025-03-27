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
