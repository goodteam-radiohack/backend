from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.event import EventEntity
from backend.domain.enum.event import EventStatus
from backend.infrastructure.database.models.base import BaseModel


class EventModel(BaseModel):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    image: Mapped[str | None] = mapped_column(nullable=True)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    status: Mapped[EventStatus] = mapped_column(
        ENUM(EventStatus, name="event_statutes"), server_default="SCHEDULED"
    )

    def to_entity(self) -> EventEntity:
        return EventEntity.model_validate(self)
