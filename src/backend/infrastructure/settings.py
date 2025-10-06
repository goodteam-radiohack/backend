from dataclasses import dataclass

from h11 import Data
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="allow")

    username: str
    password: SecretStr
    host: str = "postgres"
    port: int = 5432
    database: str

    driver: str = "psycopg"
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


@dataclass
class AppSettings:
    database: DatabaseSettings


def get_settings() -> AppSettings:
    return AppSettings(
        database=DatabaseSettings(),
    )
