from collections.abc import Iterable
from typing import Protocol

from backend.domain.dto.rsvp import CreateRsvpDTO
from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.rsvp import RSVPStatus


class RsvpReader(Protocol):
    async def with_id(self, rsvp_id: int) -> RSVPEntity: ...
    async def with_user_and_events(
        self, user_id: int, event_ids: Iterable[int]
    ) -> list[RSVPEntity]: ...

    async def with_user_and_event(self, user_id: int, event_id: int) -> RSVPEntity: ...
    async def with_event(
        self, event_id: int, status: RSVPStatus | None = None
    ) -> list[RSVPEntity]: ...


class RsvpWriter(Protocol):
    async def create(self, dto: CreateRsvpDTO) -> RSVPEntity: ...
    async def delete(self, rsvp_id: int) -> None: ...
