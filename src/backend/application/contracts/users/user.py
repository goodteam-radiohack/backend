from pydantic import BaseModel

from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole


class OmittedUserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "OmittedUserResponse":
        return OmittedUserResponse(
            id=entity.id,
            username=entity.username,
            role=entity.role,
        )


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    helping_to: OmittedUserResponse | None
    helper: OmittedUserResponse | None

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserResponse":
        return UserResponse(
            id=entity.id,
            username=entity.username,
            role=entity.role,
            helping_to=OmittedUserResponse.from_entity(entity.helping_to)
            if entity.helping_to
            else None,
            helper=OmittedUserResponse.from_entity(entity.helper)
            if entity.helper
            else None,
        )
