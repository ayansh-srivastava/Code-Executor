from fastapi import APIRouter, Request
from google.protobuf.json_format import MessageToDict

from services.api_gateway.controller import code_execution as code_execution_controller
from services.api_gateway.api_proto.decorator import proto_schema
from services.api_gateway.api_proto import code_execution_pb2
router = APIRouter()

@router.post("/execute")
@proto_schema(code_execution_pb2.ExecuteCodeRequest)
async def execute_code(request: Request):
    res = await code_execution_controller.execute_code(request)
    return MessageToDict(res)
