from fastapi import APIRouter, FastAPI

from services.core.routers.router import router
from shared.middleware.token_middleware import JWTAuthMiddleware

app = FastAPI()
core = APIRouter(prefix="/core")
core.include_router(router)
app.include_router(core)
app.add_middleware(JWTAuthMiddleware)


@app.get("/")
async def default():
    return {"page": "default"}


@app.get("/health")
async def get_health():
    return {"status": "ready"}
