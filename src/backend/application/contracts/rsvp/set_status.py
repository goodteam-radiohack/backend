from pydantic import BaseModel

from backend.domain.enum.rsvp import RSVPStatus


class SetRsvpStatusRequest(BaseModel):
    event_id: int

    status: RSVPStatus
    reason: str | None
    reason_document_id: int | None


class SetRsvpStatusResponse(BaseModel):
    success: bool
