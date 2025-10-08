from backend.domain.entities.base import BaseEntity
from backend.domain.enum.user import UserRole


class OmittedUserEntity(BaseEntity):
    id: int

    avatar_url: str | None
    name: str | None

    username: str
    password: str

    role: UserRole


class UserEntity(OmittedUserEntity):
    helping_to_id: int | None
    helping_to: OmittedUserEntity | None

    helper: OmittedUserEntity | None
