import json
import sys
import time
import uuid

from fastapi import HTTPException, Request, Response
from google.protobuf.json_format import ParseDict
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from services.api_gateway.api_proto.registry import PROTO_REGISTRY

logger.remove()
logger.add(
    sys.stdout,
    serialize=True,
    enqueue=True
)


def _decode_payload(payload: bytes):
    if not payload:
        return None

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return f"<binary payload: {len(payload)} bytes>"

    if len(text) > 10_000:
        text = f"{text[:10_000]}... <truncated>"

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _parse_json_body(payload: bytes):
    if not payload:
        return {}

    try:
        text = payload.decode("utf-8")
        body = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    return body


def _copy_response_headers(response: Response):
    return {
        key: value
        for key, value in response.headers.items()
        if key.lower() not in {"content-length", "content-encoding", "transfer-encoding"}
    }

class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.perf_counter()
        request_body = await request.body()
        request_body_log = _decode_payload(request_body)
        route_key = (request.method.upper(), request.url.path)
        proto_cls = PROTO_REGISTRY.get(route_key)

        with logger.contextualize(
            request_id=request_id,
            client_ip=request.client.host if request.client else "unknown",
            http_method=request.method,
            path=request.url.path,
        ):
            logger.bind(
                event="request_received",
                query_params=dict(request.query_params),
                headers={key: value for key, value in request.headers.items()},
                body=request_body_log,
            ).info("HTTP request received")

            try:
                if proto_cls:
                    merged_data = {
                        **_parse_json_body(request_body),
                        **dict(request.query_params),
                        **request.path_params,
                    }

                    try:
                        proto_msg = proto_cls()
                        ParseDict(merged_data, proto_msg)
                    except Exception as exc:
                        raise HTTPException(status_code=422, detail=f"Schema mismatch: {str(exc)}") from exc

                    request.state.proto = proto_msg

                response: Response = await call_next(request)
            except HTTPException as exc:
                process_time = (time.perf_counter() - start_time) * 1000
                logger.bind(
                    event="request_rejected",
                    status_code=exc.status_code,
                    duration_ms=round(process_time, 2),
                    detail=getattr(exc, "detail", None),
                ).warning("HTTP request rejected")
                raise
            except Exception:
                process_time = (time.perf_counter() - start_time) * 1000
                logger.bind(
                    event="request_failed",
                    duration_ms=round(process_time, 2),
                ).exception("HTTP request failed")
                raise

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            process_time = (time.perf_counter() - start_time) * 1000
            logger.bind(
                event="response_sent",
                status_code=response.status_code,
                duration_ms=round(process_time, 2),
                headers=dict(response.headers),
                body=_decode_payload(response_body),
            ).info("HTTP response sent")

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=_copy_response_headers(response),
                media_type=response.media_type,
                background=response.background,
            )