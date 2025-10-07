from datetime import datetime

from pydantic import BaseModel

from backend.domain.enum.event import EventStatus, EventVisibility


class CreateEventDTO(BaseModel):
    name: str
    description: str

    image: str | None

    scheduled_at: datetime
    ends_at: datetime

    status: EventStatus = EventStatus.SCHEDULED
    visibility: EventVisibility = EventVisibility.PUBLIC
    event_for_id: int | None


class UpdateEventDTO(BaseModel):
    id: int

    name: str | None = None
    description: str | None = None

    image: str | None = None

    scheduled_at: datetime | None = None
    ends_at: datetime | None = None

    status: EventStatus | None = None
