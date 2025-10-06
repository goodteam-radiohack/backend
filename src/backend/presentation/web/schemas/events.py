from typing import Self

from pydantic import BaseModel, model_validator

from backend.domain.enum.rsvp import RSVPStatus


class SetRsvpStatusSchema(BaseModel):
    status: RSVPStatus
    reason: str | None = None

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.status == RSVPStatus.NO and self.reason is None:
            raise ValueError("add reason if you selected 'no'")

        return self
