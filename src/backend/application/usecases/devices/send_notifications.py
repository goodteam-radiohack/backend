import logging
from dataclasses import dataclass
from datetime import datetime

from async_firebase import AsyncFirebaseClient
from async_firebase.messages import Message, Notification
from pytz import timezone

from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.devices.send_notification import (
    SendNotificationRequest,
)
from backend.application.gateways.device import DeviceReader
from backend.application.gateways.event import EventReader, EventUpdater
from backend.application.gateways.rsvp import RsvpReader
from backend.domain.dto.event import UpdateEventDTO
from backend.domain.enum.event import EventStatus
from backend.domain.enum.rsvp import RSVPStatus

logger = logging.getLogger(__name__)


@dataclass
class SendNotificationsUseCase(Interactor[SendNotificationRequest, None]):
    event_reader: EventReader
    event_updater: EventUpdater

    rsvp_reader: RsvpReader
    device_reader: DeviceReader

    firebase: AsyncFirebaseClient

    uow: UnitOfWork

    async def __call__(self, data: SendNotificationRequest) -> None:
        events = await self.event_reader.starting_soon()
        now = datetime.now(tz=timezone("UTC"))
        async with self.uow:
            for event in events:
                rsvps = await self.rsvp_reader.with_event(event.id, RSVPStatus.YES)
                delta = int((event.scheduled_at - now).total_seconds() / 60)

                for rsvp in rsvps:
                    user_devices = await self.device_reader.with_user_id(rsvp.user_id)

                    for device in user_devices:
                        try:
                            await self.firebase.send(
                                Message(
                                    token=device.token,
                                    notification=Notification(
                                        title="Запланированное событие вот-вот начнется",  # noqa: E501
                                        body=(
                                            f"Событие {event.name} начнется через "
                                            f"{delta} минут!"
                                        ),
                                    ),
                                )
                            )
                        except Exception:
                            logger.exception(
                                "something went wrong (while sending notification)"
                            )
                await self.event_updater.update(
                    UpdateEventDTO(id=event.id, status=EventStatus.STARTING_SOON)
                )

                await self.uow.commit()
