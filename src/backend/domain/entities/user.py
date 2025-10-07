from backend.domain.entities.base import BaseEntity
from backend.domain.enum.user import UserRole


class OmittedUserEntity(BaseEntity):
    id: int

    username: str
    password: str

    role: UserRole


class UserEntity(OmittedUserEntity):
    helping_to_id: int | None
    helping_to: OmittedUserEntity | None

    helper: OmittedUserEntity | None
