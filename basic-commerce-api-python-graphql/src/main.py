from fastapi import FastAPI
from src.db import Base, engine
from src.routes import graphql_router


app = FastAPI(
    title="Simple Commerce API - GraphQL",
    version="1.0",
)


@app.get("/healthz")
def healthz():
    return {"message": "App is health."}


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(graphql_router.router)
