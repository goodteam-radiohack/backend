from datetime import datetime

from pydantic import BaseModel

from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.rsvp.rsvp import RsvpResponse
from backend.application.contracts.users.user import UserResponse
from backend.domain.entities.event import EventEntity
from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.event import EventStatus, EventVisibility


class EventResponse(BaseModel):
    id: int

    name: str
    description: str

    image: str | None

    scheduled_at: datetime
    ends_at: datetime

    rsvp: RsvpResponse | None

    attachments: list[DocumentResponse]

    status: EventStatus
    visibility: EventVisibility

    event_for: UserResponse | None

    @classmethod
    def from_entity(
        cls,
        entity: EventEntity,
        rsvp: RSVPEntity | None = None,
        document_url: str | None = None,
    ) -> "EventResponse":
        return EventResponse(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            image=entity.image,
            scheduled_at=entity.scheduled_at,
            ends_at=entity.ends_at,
            status=entity.status,
            rsvp=RsvpResponse.from_entity(rsvp, document_url) if rsvp else None,
            attachments=[
                DocumentResponse.from_entity(item) for item in entity.attachments
            ],
            visibility=entity.visibility,
            event_for=(
                UserResponse.from_entity(entity.event_for) if entity.event_for else None
            ),
        )
