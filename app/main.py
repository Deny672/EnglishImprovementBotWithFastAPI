from fastapi import FastAPI

from app.routers.healthcheck import router as health_check
from app.routers.word import router as word

app = FastAPI()

app.include_router(health_check)
app.include_router(word)
