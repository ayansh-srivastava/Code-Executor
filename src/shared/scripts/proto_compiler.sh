#!/bin/sh

set -e

echo "Generating gRPC code..."

# Ensure script runs from project root
cd "$(dirname "$0")/../../.." || exit 1

# Activate venv for virtual python environment if it exists
# pip not supported in ubuntu 22.04, so we need to use venv
#TODO: improve and research about this
if [ -d "venv" ]; then
  . venv/bin/activate
fi

python3 -m grpc_tools.protoc \
  -I=src \
  --python_out=src \
  --grpc_python_out=src \
  src/proto/*.proto


python3 -m grpc_tools.protoc \
  -I=src \
  --python_out=src \
  --grpc_python_out=src \
  src/services/api_gateway/api_proto/*.proto

echo "Done."