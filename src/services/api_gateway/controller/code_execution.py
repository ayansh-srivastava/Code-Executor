import redis

from shared.grpc.grpc_client_manager import GrpcClientManager
from proto.code_execution_pb2 import TestConnectionRequest, ExecuteCodeRequest

redis_client = redis.StrictRedis(host='redis_server', port=6379, db=0)

async def test():
    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = TestConnectionRequest(
        message='Request from controller'
    )
    response = await code_execution_client.TestConnection(request_pb)
    return response

async def execute_code(request):
    request_body = await request.json()
    request_id = request.state.request_id
    redis_client.set(f"execution:{request_id}:status", "pending")

    print(f"Request ID: {request_id}{redis_client.get(f'execution:{request_id}:status')}")
    code_execution_client = GrpcClientManager.getInstance('code_execution')
    request_pb = ExecuteCodeRequest(
        request_id=request_id,
        version=request_body["version"],
        language=request_body.get("language"),
        code=request_body.get("code", ""),
        # stdin=request_body.get("stdin", []),
    )
    response = await code_execution_client.ExecuteCode(request_pb)
    redis_client.set(f"execution:{request_id}:status", "completed")
    print(f"Request ID: {request_id}{redis_client.get(f'execution:{request_id}:status')}")
    return response