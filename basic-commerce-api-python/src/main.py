from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.db import Base, engine
from src.routes import users_routes, products_routes, orders_routes
from .config import config_instance
from src.config import logging_instance

app = FastAPI(
    title="E-commerce API",
    version="0.0.1",
    description="Public E-commerce API",
    openapi_url="/api/v1/openapi.json",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    logging_instance.info("Tables created")


app.include_router(users_routes.router)
app.include_router(products_routes.router)
app.include_router(orders_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config_instance.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
