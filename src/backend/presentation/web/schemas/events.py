from typing import Self

from pydantic import BaseModel, model_validator

from backend.domain.enum.rsvp import RSVPStatus


class SetRsvpStatusSchema(BaseModel):
    status: RSVPStatus
    reason: str | None = None
    reason_document_id: int | None = None

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.status == RSVPStatus.NO and self.reason is None:
            raise ValueError("add reason if you selected 'no'")

        if self.status == RSVPStatus.YES and (self.reason or self.reason_document_id):
            raise ValueError("remove reason/reason_document if you selected 'yes")

        return self
