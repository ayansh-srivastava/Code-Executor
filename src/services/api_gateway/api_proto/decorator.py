def proto_schema(proto_cls):
    def decorator(func):
        setattr(func, "__proto_cls__", proto_cls)
        return func
    return decorator