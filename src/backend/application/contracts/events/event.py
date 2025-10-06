from datetime import datetime

from pydantic import BaseModel

from backend.application.contracts.rsvp.rsvp import RsvpResponse
from backend.domain.entities.event import EventEntity
from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.event import EventStatus


class EventResponse(BaseModel):
    id: int

    name: str
    description: str

    image: str | None

    scheduled_at: datetime
    ends_at: datetime

    rsvp: RsvpResponse | None

    status: EventStatus

    @classmethod
    def from_entity(
        cls, entity: EventEntity, rsvp: RSVPEntity | None = None
    ) -> "EventResponse":
        return EventResponse(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            image=entity.image,
            scheduled_at=entity.scheduled_at,
            ends_at=entity.ends_at,
            status=entity.status,
            rsvp=RsvpResponse.from_entity(rsvp) if rsvp else None,
        )
