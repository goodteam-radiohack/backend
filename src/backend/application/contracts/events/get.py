from datetime import date
from typing import Literal

from pydantic import BaseModel

from backend.domain.entities.event import EventEntity


class GetEventsRequest(BaseModel):
    period: Literal["week"]
    offset: int


class GetEventsResponse(BaseModel):
    items: dict[date, list[EventEntity]]
