from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.landings.routers import lead_router
from shared.middleware.token_middleware import JWTAuthMiddleware
from shared.redis_client.client import get_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    redis_client = get_redis_client()
    app.state.redis = redis_client
    yield
    await redis_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(lead_router.router)
app.add_middleware(JWTAuthMiddleware)


@app.get("/")
async def default():
    return {"page": "default"}


@app.get("/health")
async def get_health():
    return {"status": "ready"}
