import httpx
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import ParseDict

from proto.code_execution_pb2 import ExecuteCodeResponse

from services.code_execution.piston_adapter import PistonAdapter

class CodeExecutor():
    def __init__(self, request, context):
        self.request = request
        self.context = context
        self.piston_adapter = PistonAdapter()
        self.client = httpx.AsyncClient(
            base_url="http://piston_engine:2000",
            timeout=10.0
        )


    async def execute_code(self, request):
        response = await self.client.post(
            "/api/v2/execute",
            json=self.piston_adapter.convert_request(request)
        )

        response.raise_for_status()
        data = response.json()
        return ExecuteCodeResponse(
            output=[data.get("run", {}).get("output", "")],
        )