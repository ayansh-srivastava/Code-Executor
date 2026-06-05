from shared.grpc.grpc_client_manager import GrpcClientManager
from proto.code_execution_pb2 import TestConnectionRequest, ExecuteCodeRequest

async def test():
    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = TestConnectionRequest(
        message='Request from controller'
    )
    response = await code_execution_client.TestConnection(request_pb)
    return response

async def execute_code(request):
    request_body = await request.json()

    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = ExecuteCodeRequest(
        version=request_body["version"],
        language=request_body.get("language"),
        code=request_body.get("code", ""),
        # stdin=request_body.get("stdin", []),
    )
    response = await code_execution_client.ExecuteCode(request_pb)
    return response