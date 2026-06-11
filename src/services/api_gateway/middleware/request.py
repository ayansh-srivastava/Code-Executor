import uuid
import json
from fastapi import Request, HTTPException
from google.protobuf.json_format import ParseDict

from services.api_gateway.api_proto.registry import PROTO_REGISTRY


async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    body_bytes = await request.body()

    try:
        body_dict = json.loads(body_bytes.decode()) if body_bytes else {}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query_params = dict(request.query_params)

    path_params = request.path_params

    merged_data = {
        **body_dict,
        **query_params,
        **path_params,
    }

    route_key = (request.method.upper(), request.url.path)

    proto_cls = PROTO_REGISTRY.get(route_key)

    if not proto_cls:
        raise HTTPException(404, f"No proto schema for {route_key}")

    try:
        proto_msg = proto_cls()
        ParseDict(merged_data, proto_msg)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Schema mismatch: {str(e)}")

    request.state.proto = proto_msg

    response = await call_next(request)
    return response