from datetime import datetime
from typing import Self

from pydantic import BaseModel, model_validator
from pytz import timezone


class CreateEventRequest(BaseModel):
    name: str
    description: str

    image: str | None = None

    scheduled_at: datetime
    ends_at: datetime

    @model_validator(mode="after")
    def validate_it(self) -> Self:
        if self.scheduled_at > self.ends_at:
            raise ValueError

        if self.scheduled_at.astimezone(tz=timezone("UTC")) < datetime.now(
            tz=timezone("UTC")
        ):
            raise ValueError

        return self


class OmittedUpdateEventRequest(BaseModel):
    name: str | None = None
    description: str | None = None

    image: str | None = None

    scheduled_at: datetime | None = None
    ends_at: datetime | None = None


class UpdateEventRequest(OmittedUpdateEventRequest):
    id: int
