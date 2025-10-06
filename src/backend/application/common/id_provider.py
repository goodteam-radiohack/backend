from typing import Protocol
from uuid import UUID

from backend.domain.entities.user import UserEntity


class IdProvider(Protocol):
    async def get_user(self) -> UserEntity: ...
    async def get_session_id(self) -> UUID: ...
