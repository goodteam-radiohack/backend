from datetime import date
from typing import Literal

from pydantic import BaseModel

from backend.application.contracts.events.event import EventResponse


class GetEventRequest(BaseModel):
    id: int


class GetEventsRequest(BaseModel):
    period: Literal["week"]
    offset: int


class GetEventsResponse(BaseModel):
    items: dict[date, list[EventResponse]]
