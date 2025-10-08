import asyncio
import sys
from collections.abc import AsyncIterable
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from backend.infrastructure.ioc import get_container
from backend.infrastructure.settings import AppSettings
from backend.presentation.web import create_app

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def event_loop() -> Any:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop


@pytest_asyncio.fixture(scope="session")
async def container() -> AsyncIterable[None]:
    container = get_container(testing_environment=True)

    yield container

    await container.close()


@pytest.fixture(scope="session")
def client(container) -> Any:
    app = create_app()
    setup_dishka(container, app)

    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def alembic_cfg(container):
    cfg = AlembicConfig("alembic.ini")
    cfg.set_main_option(
        "script_location",
        str(Path("src") / "backend" / "infrastructure" / "database" / "migrations"),
    )

    config = await container.get(AppSettings)
    cfg.set_main_option("sqlalchemy.url", config.database.build_connection_uri())

    return cfg


@pytest.fixture(autouse=True, scope="session")
def run_migrations(alembic_cfg) -> None:
    upgrade(alembic_cfg, "head")
