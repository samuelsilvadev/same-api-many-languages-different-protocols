from fastapi import FastAPI, Request

from src.db import Base, engine
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
