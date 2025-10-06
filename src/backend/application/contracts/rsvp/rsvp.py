from pydantic import BaseModel

from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.rsvp import RSVPStatus


class RsvpResponse(BaseModel):
    status: RSVPStatus
    reason: str | None

    @classmethod
    def from_entity(cls, entity: RSVPEntity) -> "RsvpResponse":
        return RsvpResponse(status=entity.status, reason=entity.reason)
