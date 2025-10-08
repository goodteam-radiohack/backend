from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.application.gateways.rsvp import RsvpReader, RsvpWriter
from backend.domain.dto.rsvp import CreateRsvpDTO
from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.rsvp import RSVPStatus
from backend.infrastructure.database.models.document import DocumentModel
from backend.infrastructure.database.models.rsvp import RSVPModel
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.rsvp import RsvpNotFoundError

_OPTIONS = [
    joinedload(RSVPModel.reason_document)
    .joinedload(DocumentModel.created_by)
    .joinedload(UserModel.helper),
    joinedload(RSVPModel.reason_document)
    .joinedload(DocumentModel.created_by)
    .joinedload(UserModel.helping_to),
]


@dataclass
class RsvpGateway(RsvpReader, RsvpWriter):
    session: AsyncSession

    async def with_id(self, rsvp_id: int) -> RSVPEntity:
        stmt = select(RSVPModel).where(RSVPModel.id == rsvp_id).options(*_OPTIONS)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise RsvpNotFoundError from exc

        return result.to_entity()

    async def with_user_and_events(
        self, user_id: int, event_ids: Iterable[int]
    ) -> list[RSVPEntity]:
        stmt = (
            select(RSVPModel)
            .where(RSVPModel.user_id == user_id, RSVPModel.event_id.in_(event_ids))
            .options(*_OPTIONS)
        )

        results = (await self.session.scalars(stmt)).all()

        return [result.to_entity() for result in results]

    async def with_user_and_event(self, user_id: int, event_id: int) -> RSVPEntity:
        stmt = (
            select(RSVPModel)
            .where(RSVPModel.event_id == event_id, RSVPModel.user_id == user_id)
            .options(*_OPTIONS)
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise RsvpNotFoundError from exc

        return result.to_entity()

    async def with_event(
        self, event_id: int, status: RSVPStatus | None = None
    ) -> list[RSVPEntity]:
        stmt = select(RSVPModel).where(RSVPModel.event_id == event_id)

        if status is not None:
            stmt = stmt.where(RSVPModel.status == status)

        results = (await self.session.scalars(stmt)).all()
        return [result.to_entity() for result in results]

    async def create(self, dto: CreateRsvpDTO) -> RSVPEntity:
        stmt = insert(RSVPModel).values(**dto.model_dump()).returning(RSVPModel.id)

        rsvp_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(rsvp_id)

    async def delete(self, rsvp_id: int) -> None:
        stmt = delete(RSVPModel).where(RSVPModel.id == rsvp_id)
        await self.session.execute(stmt)
