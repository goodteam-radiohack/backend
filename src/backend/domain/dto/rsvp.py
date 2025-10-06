from pydantic import BaseModel

from backend.domain.enum.rsvp import RSVPStatus


class CreateRsvpDTO(BaseModel):
    event_id: int
    user_id: int

    status: RSVPStatus
    reason: str | None
    reason_document_id: int | None
