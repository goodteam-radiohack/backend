from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.gateways.rsvp import RsvpReader, RsvpWriter
from backend.domain.dto.rsvp import CreateRsvpDTO
from backend.domain.entities.rsvp import RSVPEntity
from backend.infrastructure.database.models.rsvp import RSVPModel
from backend.infrastructure.errors.gateways.rsvp import RsvpNotFoundError


@dataclass
class RsvpGateway(RsvpReader, RsvpWriter):
    session: AsyncSession

    async def with_id(self, rsvp_id: int) -> RSVPEntity:
        stmt = select(RSVPModel).where(RSVPModel.id == rsvp_id)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise RsvpNotFoundError from exc

        return result.to_entity()

    async def create(self, dto: CreateRsvpDTO) -> RSVPEntity:
        stmt = insert(RSVPModel).values(**dto.model_dump()).returning(RSVPModel.id)

        rsvp_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(rsvp_id)

    async def delete(self, rsvp_id: int) -> None:
        stmt = delete(RSVPModel).where(RSVPModel.id == rsvp_id)
        await self.session.execute(stmt)
