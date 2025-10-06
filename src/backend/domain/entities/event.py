from datetime import datetime

from backend.domain.entities.base import BaseEntity
from backend.domain.enum.event import EventStatus


class EventEntity(BaseEntity):
    id: int

    name: str
    description: str

    image: str | None

    scheduled_at: datetime
    ends_at: datetime

    status: EventStatus
