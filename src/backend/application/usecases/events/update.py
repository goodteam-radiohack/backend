from dataclasses import dataclass
from datetime import datetime, timedelta

from pytz import timezone

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.events.create import UpdateEventRequest
from backend.application.contracts.events.event import EventResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.event import EventReader, EventUpdater
from backend.domain.dto.event import UpdateEventDTO
from backend.domain.enum.event import EventStatus
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

            new_status = event.status
            if event.status == EventStatus.STARTING_SOON:
                if event.scheduled_at - datetime.now(tz=timezone("UTC")) >= timedelta(
                    minutes=1
                ):
                    new_status = EventStatus.SCHEDULED
                elif event.ends_at - datetime.now(tz=timezone("UTC")) <= timedelta(
                    seconds=0
                ):
                    new_status = EventStatus.ENDED
                else:
                    new_status = EventStatus.IN_PROCESS

            event = await self.event_updater.update(
                UpdateEventDTO(id=event.id, status=new_status)
            )

            await self.uow.commit()

        return EventResponse.from_entity(event)
