from fastapi import FastAPI
from fastapi.routing import APIRoute
from services.api_gateway.api_proto.registry import PROTO_REGISTRY


def load_proto_registry(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoint = route.endpoint

            proto_cls = getattr(endpoint, "__proto_cls__", None)
            if proto_cls:
                for method in route.methods:
                    key = (method.upper(), route.path)
                    PROTO_REGISTRY[key] = proto_cls