from collections.abc import Iterator

from dishka import Provider, Scope, provide
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from backend.infrastructure.settings import (
    AppSettings,
    DatabaseSettings,
    GoogleSettings,
    NatsSettings,
    RedisSettings,
    S3Settings,
    WebSettings,
    get_settings,
)


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_settings(self) -> AppSettings:
        return get_settings()


class TestSettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_settings(self) -> Iterator[AppSettings]:
        postgres = PostgresContainer(image="postgres:17.2-alpine", driver="asyncpg")
        redis = RedisContainer(image="redis:7.4.1-alpine")

        postgres.start()
        redis.start()

        yield AppSettings(
            database=DatabaseSettings(
                username=postgres.username,
                password=postgres.password,
                host=postgres.get_container_host_ip(),
                database=postgres.dbname,
                port=postgres.get_exposed_port(5432),
            ),
            redis=RedisSettings(
                host=redis.get_container_host_ip(),
                port=redis.get_exposed_port(6379),
            ),
            s3=S3Settings(endpoint="", bucket="", access_key="", secret_key=""),
            web=WebSettings(jwt_secret="super_secret"),
            nats=NatsSettings(url="nats://127.0.0.1"),
            google=GoogleSettings(data={}),
        )

        postgres.stop()
        redis.stop()
