from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import exists, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.application.gateways.event import EventReader, EventUpdater, EventWriter
from backend.domain.dto.event import CreateEventDTO, UpdateEventDTO
from backend.domain.entities.event import EventEntity
from backend.domain.enum.event import EventVisibility
from backend.infrastructure.database.models.document import DocumentModel
from backend.infrastructure.database.models.event import EventModel
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.event import EventNotFoundError

_OPTIONS = [
    selectinload(EventModel.attachments).joinedload(DocumentModel.created_by),
    joinedload(EventModel.event_for).joinedload(UserModel.helper),
    joinedload(EventModel.event_for).joinedload(UserModel.helping_to),
]


@dataclass
class EventGateway(EventReader, EventWriter, EventUpdater):
    session: AsyncSession

    async def with_id(self, event_id: int) -> EventEntity:
        stmt = select(EventModel).where(EventModel.id == event_id).options(*_OPTIONS)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise EventNotFoundError from exc

        return result.to_entity()

    async def all_window(
        self, start: datetime, end: datetime, user_id: int
    ) -> list[EventEntity]:
        stmt = (
            select(EventModel)
            .where(
                EventModel.scheduled_at >= start,
                EventModel.scheduled_at < end,
                (
                    (EventModel.visibility == EventVisibility.PUBLIC)
                    | (
                        (EventModel.visibility == EventVisibility.PRIVATE)
                        & (EventModel.event_for_id == user_id)
                    )
                ),
            )
            .order_by(EventModel.scheduled_at)
            .options(*_OPTIONS)
        )

        results = (await self.session.scalars(stmt)).all()

        return [result.to_entity() for result in results]

    async def exists(self, event_id: int) -> bool:
        stmt = select(exists(EventModel).where(EventModel.id == event_id))
        return (await self.session.scalars(stmt)).one()

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
