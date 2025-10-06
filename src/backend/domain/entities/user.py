from backend.domain.entities.base import BaseEntity
from backend.domain.enum.user import UserRole


class UserEntity(BaseEntity):
    id: int

    username: str
    password: str

    role: UserRole
