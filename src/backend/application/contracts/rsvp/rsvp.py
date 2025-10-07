from pydantic import BaseModel

from backend.application.contracts.documents.document import DocumentResponse
from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.rsvp import RSVPStatus


class RsvpResponse(BaseModel):
    status: RSVPStatus
    reason: str | None
    reason_document: DocumentResponse | None

    @classmethod
    def from_entity(
        cls, entity: RSVPEntity, document_url: str | None
    ) -> "RsvpResponse":
        return RsvpResponse(
            status=entity.status,
            reason=entity.reason,
            reason_document=(
                DocumentResponse.from_entity(entity.reason_document, document_url)
                if entity.reason_document
                else None
            ),
        )
