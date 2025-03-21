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
