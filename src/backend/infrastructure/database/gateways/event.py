from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.gateways.event import EventReader, EventUpdater, EventWriter
from backend.domain.dto.event import CreateEventDTO, UpdateEventDTO
from backend.domain.entities.event import EventEntity
from backend.infrastructure.database.models.event import EventModel
from backend.infrastructure.errors.gateways.event import EventNotFoundError


@dataclass
class EventGateway(EventReader, EventWriter, EventUpdater):
    session: AsyncSession

    async def with_id(self, event_id: int) -> EventEntity:
        stmt = select(EventModel).where(EventModel.id == event_id)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise EventNotFoundError from exc

        return result.to_entity()

    async def all_window(self, start: datetime, end: datetime) -> list[EventEntity]:
        stmt = select(EventModel).where(
            EventModel.scheduled_at >= start, EventModel.scheduled_at < end
        )

        results = (await self.session.scalars(stmt)).all()

        return [result.to_entity() for result in results]

    async def create(self, dto: CreateEventDTO) -> EventEntity:
        stmt = insert(EventModel).values(**dto.model_dump()).returning(EventModel.id)

        event_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(event_id)

    async def update(self, dto: UpdateEventDTO) -> EventEntity:
        stmt = (
            update(EventModel)
            .values(**dto.model_dump(exclude={"id"}, exclude_unset=True))
            .where(EventModel.id == dto.id)
        )

        await self.session.execute(stmt)

        return await self.with_id(dto.id)
