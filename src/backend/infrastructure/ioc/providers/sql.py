from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.infrastructure.settings import AppSettings


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, settings: AppSettings) -> AsyncEngine:
        return create_async_engine(
            url=settings.database.build_connection_uri(),
            poolclass=AsyncAdaptedQueuePool,
            pool_size=30,
            max_overflow=20,
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
