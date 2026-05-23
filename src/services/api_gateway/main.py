from fastapi import FastAPI
from services.api_gateway.routes import health

app = FastAPI()

api_router = FastAPI()

app.include_router(health.router, prefix="/api/health", tags=["health"])