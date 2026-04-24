from fastapi import FastAPI

from services.landings.routers import lead_router
from shared.middleware.token_middleware import JWTAuthMiddleware

app = FastAPI()
app.include_router(lead_router.router)
app.add_middleware(JWTAuthMiddleware)


@app.get("/")
async def default():
    return {"page": "default"}


@app.get("/health")
async def get_health():
    return {"status": "ready"}
