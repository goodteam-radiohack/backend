from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.events.create import UpdateEventRequest
from backend.application.contracts.events.event import EventResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.event import EventReader, EventUpdater
from backend.domain.dto.event import UpdateEventDTO
from backend.domain.enum.user import UserRole


@dataclass
class UpdateEventUseCase(Interactor[UpdateEventRequest, EventResponse]):
    id_provider: IdProvider

    event_reader: EventReader
    event_updater: EventUpdater

    uow: UnitOfWork

    async def __call__(self, data: UpdateEventRequest) -> EventResponse:
        user = await self.id_provider.get_user()
        event = await self.event_reader.with_id(data.id)

        if user.role != UserRole.ADMIN and not event.has_access(user):
            raise UnauthorizedError

        # TODO: use `exists` query

        async with self.uow:
            event = await self.event_updater.update(
                UpdateEventDTO(
                    id=data.id,
                    **data.model_dump(
                        exclude={"id"},
                        exclude_unset=True,
                    ),
                )
            )

            await self.uow.commit()

        return EventResponse.from_entity(event)
