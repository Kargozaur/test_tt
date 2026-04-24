from fastapi import FastAPI

from services.core.routers.router import router

app = FastAPI()
app.include_router(router)
