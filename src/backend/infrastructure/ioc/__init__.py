from dishka import AsyncContainer, make_async_container

from backend.infrastructure.ioc.providers.gateways import GatewaysProvider
from backend.infrastructure.ioc.providers.settings import SettingsProvider
from backend.infrastructure.ioc.providers.sql import SQLAlchemyProvider
from backend.infrastructure.ioc.providers.usecases import UsecasesProvider


def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SQLAlchemyProvider(),
        GatewaysProvider(),
        UsecasesProvider(),
    )
