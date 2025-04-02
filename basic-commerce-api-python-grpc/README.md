## Running locally

```shell
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8001
```

### Format Files

```shell
    uv run ruff format
```

### Migration

#### Create migration

```shell
  uv run alembic revision --autogenerate -m "your amazing message"
```

#### Run migration

```shell
  uv run alembic upgrade head
```

#### Protobuf

Generate the protobuf files

```shell
  python3 -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated ./proto/users.proto
```
