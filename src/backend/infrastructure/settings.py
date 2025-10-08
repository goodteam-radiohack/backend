from dataclasses import dataclass
from datetime import timedelta

from pydantic import NatsDsn, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class WebSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WEB_", env_file=".env", extra="allow")

    jwt_secret: SecretStr
    jwt_expires_in: timedelta = timedelta(days=30)


class GoogleSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GOOGLE_", env_file=".env", extra="allow"
    )

    data: dict[str, str]


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="S3_", env_file=".env", extra="allow")

    region: str | None = None

    endpoint: str
    bucket: str

    access_key: SecretStr
    secret_key: SecretStr


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="allow")

    username: str
    password: SecretStr
    host: str = "postgres"
    port: int = 5432
    database: str

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_uri(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.database_system}+{self.driver}",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.database,
        )
        return dsn.unicode_string()


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_", env_file=".env", extra="allow"
    )

    username: str | None = None
    password: SecretStr | None = None

    host: str = "127.0.0.1"
    port: int = 6379
    database: str = "0"

    def build_connection_uri(self) -> str:
        dsn: RedisDsn = RedisDsn.build(
            scheme="redis",
            username=self.username,
            password=self.password.get_secret_value() if self.password else None,
            path=self.database,
            host=self.host,
            port=self.port,
        )

        return dsn.unicode_string()


class NatsSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NATS_", env_file=".env", extra="allow"
    )

    url: NatsDsn

    def build_connection_uri(self) -> str:
        return self.url.unicode_string()


@dataclass
class AppSettings:
    database: DatabaseSettings
    redis: RedisSettings
    web: WebSettings
    nats: NatsSettings
    google: GoogleSettings

    s3: S3Settings


def get_settings() -> AppSettings:
    return AppSettings(
        database=DatabaseSettings(),
        redis=RedisSettings(),
        web=WebSettings(),
        s3=S3Settings(),
        nats=NatsSettings(),
        google=GoogleSettings(),
    )
