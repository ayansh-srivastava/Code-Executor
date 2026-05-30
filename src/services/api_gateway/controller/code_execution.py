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
    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = ExecuteCodeRequest(

    )
    response = await code_execution_client.ExecuteCode(request_pb)
    return response