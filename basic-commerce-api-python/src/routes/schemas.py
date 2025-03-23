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
