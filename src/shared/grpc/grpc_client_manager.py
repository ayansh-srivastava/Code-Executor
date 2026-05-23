from grpc import aio
import importlib
from threading import Lock
from shared.grpc.grpc_config import GRPC_SERVICES


class GrpcClientManager:
    _instances = {}
    _lock = Lock()

    def __init__(self):
        self._clients = {}
        self._channels = {}

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = cls()
        return cls._instance

    def get_client(self, service_name: str):
        if service_name in self._clients:
            return self._clients[service_name]

        if service_name not in GRPC_SERVICES:
            raise ValueError(f"Service '{service_name}' not configured")

        config = GRPC_SERVICES[service_name]

        # Create channel
        channel = aio.insecure_channel(config["address"])

        # Dynamically import stub
        module = importlib.import_module(config["module"])
        stub_class = getattr(module, config["stub_class"])

        # Create stub
        client = stub_class(channel)

        # Cache
        self._clients[service_name] = client
        self._channels[service_name] = channel

        return client

    @classmethod
    def getInstance(cls, service_name: str):
        return cls.get_instance().get_client(service_name)

    async def close_all(self):
        for channel in self._channels.values():
            await channel.close()

#TODO Add Interceptors (auth, logging)