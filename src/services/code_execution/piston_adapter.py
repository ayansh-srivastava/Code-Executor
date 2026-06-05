from proto import code_execution_pb2

languageMap = {
    "PYTHON": {"name": "python", "filename": "Main.py"},
    "JAVASCRIPT": {"name": "javascript", "filename": "Main.js"},
    "JAVA": {"name": "java", "filename": "Main.java"},
    "C": {"name": "c", "filename": "Main.c"},
    "CPP": {"name": "cpp", "filename": "Main.cpp"}
}

class PistonAdapter:
    def __init__(self):
        pass

    def convert_request(self, request):
        # Convert the coming request to the format expected by piston engine
        return {
            "language": str(languageMap.get(code_execution_pb2.ExecuteCodeRequest.Language.Name(request.language))["name"]),
            "version": str(request.version),
            "files": [
                {
                    "name": str(languageMap.get(code_execution_pb2.ExecuteCodeRequest.Language.Name(request.language)).get("filename", "Main")),
                    "content": str(request.code)
                }
            ],
            "stdin": str(request.stdin),
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 3000,
            "compile_cpu_time": 10000,
            "run_cpu_time": 3000,
            "compile_memory_limit": -1,
            "run_memory_limit": -1
        }
