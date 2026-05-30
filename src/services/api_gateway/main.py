from fastapi import FastAPI
from services.api_gateway.routes import health
from services.api_gateway.routes import code_execution

app = FastAPI()

api_router = FastAPI()

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(code_execution.router, prefix="/api/code-execution", tags=["code-execution"])
