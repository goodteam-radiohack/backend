from typing import Protocol

from backend.domain.dto.user import CreateUserDTO
from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole


class UserReader(Protocol):
    async def with_id(self, user_id: int) -> UserEntity: ...
    async def with_username(self, username: str) -> UserEntity: ...

    async def all(self, limit: int, offset: int) -> tuple[list[UserEntity], int]: ...


class UserWriter(Protocol):
    async def create(self, dto: CreateUserDTO) -> UserEntity: ...


class UserUpdater(Protocol):
    async def update_role(self, user_id: int, role: UserRole) -> UserEntity: ...
