from pydantic import BaseModel

from backend.domain.entities.user import OmittedUserEntity, UserEntity
from backend.domain.enum.user import UserRole


class OmittedUserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    avatar_url: str | None
    name: str | None

    @classmethod
    def from_entity(cls, entity: OmittedUserEntity) -> "OmittedUserResponse":
        return OmittedUserResponse(
            id=entity.id,
            username=entity.username,
            role=entity.role,
            avatar_url=entity.avatar_url,
            name=entity.name,
        )


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    helping_to: OmittedUserResponse | None
    helper: OmittedUserResponse | None

    avatar_url: str | None
    name: str | None

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
            avatar_url=entity.avatar_url,
            name=entity.name,
        )
