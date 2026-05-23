import asyncio
import logging

from grpc import aio

from proto import code_execution_pb2_grpc as CodeExecutionService
from proto.code_execution_pb2 import TestConnectionResponse

class CodeExecution(CodeExecutionService.CodeExecutionServicer):

    async def test_connection(self, request, context):
        return TestConnectionResponse(message = 'Hi connection is good')

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