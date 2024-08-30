from fastapi import FastAPI
from app.routers.healthcheck import router as health_check

app = FastAPI()

app.include_router(health_check)