from typing import List
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import APIRouter
from src.routes.schemas import CreateUserPayload, CreateUserResponse, GetUserResponse

from src.db import get_session
from src.repository import users_repository


@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[GetUserResponse]:
        db = get_session()
        users = users_repository.get_all_users(db)

        return [
            GetUserResponse(id=user.id, name=user.name, email=user.email)
            for user in users
        ]

    @strawberry.field
    async def user_by_id(self, id: int) -> GetUserResponse:
        db = get_session()
        user = users_repository.get_user_by_id(db, id)

        if user is None:
            raise Exception("User not found")

        return GetUserResponse(id=user.id, name=user.name, email=user.email)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self, name: str, email: str, password: str
    ) -> CreateUserResponse:
        db = get_session()
        new_user = users_repository.create_user(
            db, CreateUserPayload(name=name, email=email, password=password)
        )

        return CreateUserResponse(
            id=new_user.id, name=new_user.name, email=new_user.email
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)


router = APIRouter()
router.include_router(GraphQLRouter(schema), prefix="/api")
