from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.infrastructure.ioc import get_container
from backend.presentation.web.routes import setup_routes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container: AsyncContainer = app.state.dishka_container

    yield

    await container.close()


def create_app() -> FastAPI:
    app = FastAPI(title="DumaHelper", lifespan=lifespan)

    container = get_container()
    setup_dishka(container, app)

    setup_routes(app)

    return app
