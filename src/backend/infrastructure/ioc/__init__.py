from dishka import AsyncContainer, make_async_container

from backend.infrastructure.ioc.providers.adapters import FirebaseProvider, S3Provider
from backend.infrastructure.ioc.providers.auth import AuthProvider
from backend.infrastructure.ioc.providers.gateways import GatewaysProvider
from backend.infrastructure.ioc.providers.redis import RedisProvider
from backend.infrastructure.ioc.providers.settings import (
    SettingsProvider,
    TestSettingsProvider,
)
from backend.infrastructure.ioc.providers.sql import SQLAlchemyProvider
from backend.infrastructure.ioc.providers.usecases import UsecasesProvider


def get_container(testing_environment: bool = False) -> AsyncContainer:
    providers = [
        SQLAlchemyProvider(),
        RedisProvider(),
        GatewaysProvider(),
        UsecasesProvider(),
        AuthProvider(),
        S3Provider(),
        FirebaseProvider(),
    ]

    if not testing_environment:
        return make_async_container(
            *providers,
            SettingsProvider(),
        )

    return make_async_container(
        *providers,
        TestSettingsProvider(),
    )
