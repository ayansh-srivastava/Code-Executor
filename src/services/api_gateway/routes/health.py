from fastapi import APIRouter
from google.protobuf.json_format import MessageToDict

from services.api_gateway.controller import code_execution as code_execution_controller

router = APIRouter()

@router.get("/health")
def read():
    return {"message": "Welcome to FastAPI!"}

@router.get("/testCodeExecution")
async def test():
    res = await code_execution_controller.test()
    return MessageToDict(res)
