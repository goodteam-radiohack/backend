from pydantic import BaseModel

from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserResponse":
        return UserResponse(
            id=entity.id,
            username=entity.username,
            role=entity.role,
        )
