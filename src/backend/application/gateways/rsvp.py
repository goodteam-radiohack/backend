from typing import Protocol

from backend.domain.dto.rsvp import CreateRsvpDTO
from backend.domain.entities.rsvp import RSVPEntity


class RsvpReader(Protocol):
    async def with_id(self, rsvp_id: int) -> RSVPEntity: ...


class RsvpWriter(Protocol):
    async def create(self, dto: CreateRsvpDTO) -> RSVPEntity: ...
    async def delete(self, rsvp_id: int) -> None: ...
