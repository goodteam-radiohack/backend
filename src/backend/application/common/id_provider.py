from typing import Protocol

from backend.domain.entities.user import UserEntity


class IdProvider(Protocol):
    async def get_user(self) -> UserEntity: ...
