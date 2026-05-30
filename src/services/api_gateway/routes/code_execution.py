from fastapi import APIRouter, Request
from google.protobuf.json_format import MessageToDict

from services.api_gateway.controller import code_execution as code_execution_controller

router = APIRouter()

@router.post("/execute")
async def execute_code(request: Request):
    res = await code_execution_controller.execute_code(request)
    return MessageToDict(res)
