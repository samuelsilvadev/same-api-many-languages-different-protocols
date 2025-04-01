import strawberry
from typing import List
from src.routes.schemas import CreateUserPayload, CreateUserResponse, GetUserResponse

from src.db import get_session
from src.repository import users_repository
from src.config import logging_instance


@strawberry.type
class UsersQueries:
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
class UsersMutations:
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

    @strawberry.mutation
    async def delete_user(self, id: int) -> None:
        db = get_session()
        user_to_delete = users_repository.get_user_by_id(db, id)

        if user_to_delete is None:
            raise Exception("User not found")

        try:
            users_repository.delete_user(db, user_to_delete)
        except Exception as error:
            logging_instance.error(error)

            if isinstance(error, Exception):
                raise error

            raise Exception("Failed to delete user")
