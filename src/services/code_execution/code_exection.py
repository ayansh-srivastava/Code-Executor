import httpx
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import ParseDict

from proto.code_execution_pb2 import ExecuteCodeResponse

class CodeExecutor():
    def __init__(self, request, context):
        self.request = request
        self.context = context
        self.client = httpx.AsyncClient(
            base_url="http://piston_engine:2000",
            timeout=10.0
        )


    async def execute_code(self, request):
        response = await self.client.post(
            "/api/v2/execute",
            json={
                # "language": request.language,
                # "version": request.version,
                # "files": [
                #     {
                #         "name": request.filename,
                #         "content": request.code
                #     }
                # ],
                "language": "java",
            "version": "15.0.2",
            "files": [
                {
                "name": "Main.java",
                "content": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Java is working!\");\n    }\n}"
                }
            ]
            }
        )

        response.raise_for_status()
        data = response.json()

        return ExecuteCodeResponse(
            output=[ParseDict(data.get("run", {}), Struct())],
        )