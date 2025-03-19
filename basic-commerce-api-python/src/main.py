import src.initializers as initializers
from fastapi import FastAPI, Request
from .config import config_instance

app = FastAPI(
    title="E-commerce API",
    version="0.0.1",
    description="Public E-commerce API",
    openapi_url="/api/v1/openapi.json",
)


@app.get("/health")
async def health():
    return {"status": "ok"}
