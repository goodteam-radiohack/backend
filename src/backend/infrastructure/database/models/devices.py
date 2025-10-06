from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.enum.device import Platform
from backend.infrastructure.database.models.base import BaseModel
from backend.infrastructure.database.models.user import UserModel


class DeviceModel(BaseModel):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship()

    token: Mapped[str] = mapped_column(unique=True)
    platform: Mapped[Platform] = mapped_column(ENUM(Platform, name="platforms"))

    # TODO: add `expires_at` field
