from datetime import datetime
from typing import Protocol

from backend.domain.dto.event import CreateEventDTO, UpdateEventDTO
from backend.domain.entities.event import EventEntity


class EventReader(Protocol):
    async def with_id(self, event_id: int) -> EventEntity: ...
    async def all_window(
        self, start: datetime, end: datetime, user_id: int
    ) -> list[EventEntity]: ...

    async def exists(self, event_id: int) -> bool: ...


class EventWriter(Protocol):
    async def create(self, dto: CreateEventDTO) -> EventEntity: ...


class EventUpdater(Protocol):
    async def update(self, dto: UpdateEventDTO) -> EventEntity: ...
