import asyncio
import logging

from grpc import aio

from proto import code_execution_pb2_grpc as CodeExecutionService
from proto.code_execution_pb2 import TestConnectionResponse

from services.code_execution.code_exection import CodeExecutor

class CodeExecution(CodeExecutionService.CodeExecutionServicer):

    async def TestConnection(self, request, context):
        return TestConnectionResponse(message = 'Hi connection is good')

    async def ExecuteCode(self, request, context):
        code_executor = CodeExecutor(request, context)
        return await code_executor.execute_code(request)

async def serve():
    server = aio.server()
    listen_addr = "[::]:50051"
    CodeExecutionService.add_CodeExecutionServicer_to_server(
        CodeExecution(), server
    )
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    print("gRPC server started")
    asyncio.run(serve())