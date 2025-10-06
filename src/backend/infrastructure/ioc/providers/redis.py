from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from backend.infrastructure.settings import AppSettings


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_redis(self, settings: AppSettings) -> AsyncIterator[Redis]:
        async with Redis.from_url(settings.redis.build_connection_uri()) as client:
            yield client
