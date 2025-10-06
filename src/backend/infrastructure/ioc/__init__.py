from dishka import AsyncContainer, make_async_container

from backend.infrastructure.ioc.providers.adapters import S3Provider
from backend.infrastructure.ioc.providers.auth import AuthProvider
from backend.infrastructure.ioc.providers.gateways import GatewaysProvider
from backend.infrastructure.ioc.providers.redis import RedisProvider
from backend.infrastructure.ioc.providers.settings import SettingsProvider
from backend.infrastructure.ioc.providers.sql import SQLAlchemyProvider
from backend.infrastructure.ioc.providers.usecases import UsecasesProvider


def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SQLAlchemyProvider(),
        RedisProvider(),
        GatewaysProvider(),
        UsecasesProvider(),
        AuthProvider(),
        S3Provider(),
    )
