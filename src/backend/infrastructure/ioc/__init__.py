from dishka import AsyncContainer, make_async_container

from backend.infrastructure.ioc.providers.settings import SettingsProvider
from backend.infrastructure.ioc.providers.sql import SQLAlchemyProvider


def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SQLAlchemyProvider(),
    )
