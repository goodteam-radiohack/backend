from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.events.create import CreateEventRequest
from backend.application.contracts.events.event import EventResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.event import EventWriter
from backend.domain.dto.event import CreateEventDTO
from backend.domain.enum.event import EventVisibility
from backend.domain.enum.user import UserRole


@dataclass
class CreateEventUseCase(Interactor[CreateEventRequest, EventResponse]):
    id_provider: IdProvider

    event_writer: EventWriter

    uow: UnitOfWork

    async def __call__(self, data: CreateEventRequest) -> EventResponse:
        user = await self.id_provider.get_user()

        if user.role != UserRole.ADMIN and data.visibility == EventVisibility.PUBLIC:
            raise UnauthorizedError("only admins can create public events")

        event_for_id = user.helping_to_id or user.id

        async with self.uow:
            event = await self.event_writer.create(
                CreateEventDTO(
                    name=data.name,
                    description=data.description,
                    image=data.image,
                    scheduled_at=data.scheduled_at,
                    ends_at=data.ends_at,
                    event_for_id=(
                        None
                        if user.role == UserRole.ADMIN
                        and data.visibility == EventVisibility.PUBLIC
                        else event_for_id
                    ),
                    visibility=data.visibility,
                )
            )

            await self.uow.commit()

        return EventResponse.from_entity(event)
