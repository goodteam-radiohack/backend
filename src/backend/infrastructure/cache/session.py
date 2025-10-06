from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis

from backend.infrastructure.errors.cache.session import (
    SessionExpiredError,
    SessionNotFoundError,
)


@dataclass
class SessionGateway:
    redis: Redis

    KEY = "session:{uuid}"
    LOGGED_OUT_KEY = "session:{uuid}:is_logout"

    async def with_id(self, session_uuid: UUID) -> int:
        """Get client_id via session uuid"""
        is_logged_out = await self.redis.get(
            self.LOGGED_OUT_KEY.format(uuid=session_uuid)
        )

        if is_logged_out:
            raise SessionExpiredError

        client_id = await self.redis.get(self.KEY.format(uuid=session_uuid))
        if client_id is None:
            raise SessionNotFoundError

        return int(client_id)

    async def create(self, client_id: int, expires: timedelta) -> UUID:
        session_uuid = uuid4()
        await self.redis.set(self.KEY.format(uuid=session_uuid), client_id, ex=expires)
        return session_uuid

    async def logout(self, session_uuid: UUID) -> None:
        await self.redis.set(self.LOGGED_OUT_KEY.format(uuid=session_uuid), 1)
