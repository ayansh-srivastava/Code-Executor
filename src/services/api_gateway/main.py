from fastapi import FastAPI
from services.api_gateway.proto_registry_loader import load_proto_registry
from services.api_gateway.middleware.request import RequestMiddleware
from services.api_gateway.routes import health
from services.api_gateway.routes import code_execution

app = FastAPI()

api_router = FastAPI()

app.add_middleware(RequestMiddleware)

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(code_execution.router, prefix="/api/code-execution", tags=["code-execution"])

@app.on_event("startup")
async def startup_event():
    load_proto_registry(app)