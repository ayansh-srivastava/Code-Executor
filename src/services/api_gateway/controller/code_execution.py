from shared.grpc.grpc_client_manager import GrpcClientManager
from proto.code_execution_pb2 import TestConnectionRequest

async def test():
    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = TestConnectionRequest(
        message='Request from controller'
    )
    response = await code_execution_client.test_connection(request_pb)
    return response