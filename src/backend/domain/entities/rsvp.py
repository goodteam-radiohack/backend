from backend.domain.entities.base import BaseEntity
from backend.domain.entities.document import DocumentEntity
from backend.domain.enum.rsvp import RSVPStatus


class RSVPEntity(BaseEntity):
    id: int

    event_id: int
    user_id: int

    status: RSVPStatus
    reason: str | None
    reason_document: DocumentEntity | None
