from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole
from backend.infrastructure.database.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()

    role: Mapped[UserRole] = mapped_column(ENUM(UserRole, name="user_roles"))

    def to_entity(self) -> UserEntity:
        return UserEntity.model_validate(self)
