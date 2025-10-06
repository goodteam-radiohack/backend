# How to...

# Prerequisites

- Python 3.13+
- PostgreSQL с созданной БД
- Установлен uv

## Init application

```shell
uv sync
uv pip install -e .
```

## Apply migrations

```shell
uv run alembic upgrade head
```

## Generate migration

```shell
uv run alembic revision --autogenerate -m "<message here>"
```

## Run application

Dev:

```shell
uv run uvicorn --factory --host 127.0.0.1 --port 8080 backend.presentation.web:create_app
```

## Troubleshooting

- Проверь доступность DATABASE_URL
