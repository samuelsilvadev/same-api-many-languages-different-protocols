import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import APIRouter

from src.routes.users import UsersMutations, UsersQueries


@strawberry.type
class Query(UsersQueries):
    pass


@strawberry.type
class Mutation(UsersMutations):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
router = APIRouter()
router.include_router(GraphQLRouter(schema), prefix="/api")
