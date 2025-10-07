from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from pytz import timezone

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.events.event import EventResponse
from backend.application.contracts.events.get import GetEventsRequest, GetEventsResponse
from backend.application.gateways.event import EventReader
from backend.application.gateways.rsvp import RsvpReader
from backend.domain.services.s3 import S3Service

TZ = timezone("Asia/Yekaterinburg")
EXPIRES_IN = timedelta(hours=3)


@dataclass
class GetEventsUseCase(Interactor[GetEventsRequest, GetEventsResponse]):
    id_provider: IdProvider

    s3_service: S3Service

    rsvp_reader: RsvpReader
    event_reader: EventReader

    def _week_range(self, offset: int) -> tuple[datetime, datetime]:
        now = datetime.now(tz=TZ)

        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
            days=now.weekday()
        )
        start += timedelta(weeks=offset)
        end_exclusive = start + timedelta(weeks=1)

        return start, end_exclusive

    async def __call__(self, data: GetEventsRequest) -> GetEventsResponse:
        user = await self.id_provider.get_user()

        # TODO: add depute status at every event

        start, end = self._week_range(data.offset)

        events = await self.event_reader.all_window(
            start, end, user.helping_to_id or user.id
        )
        grouped_events = defaultdict(list)

        # TODO: это можно оптимизировать немного)
        items: list[EventResponse] = []
        rsvps = await self.rsvp_reader.with_user_and_events(
            user.id, {event.id for event in events}
        )

        for event in events:
            rsvp = next(filter(lambda x: x.event_id == event.id, rsvps), None)
            document_url = (
                await self.s3_service.get_url(
                    rsvp.reason_document.storage_key, EXPIRES_IN
                )
                if rsvp and rsvp.reason_document
                else None
            )

            items.append(EventResponse.from_entity(event, rsvp, document_url))

        for item in items:
            grouped_events[item.scheduled_at.astimezone(tz=TZ).date()].append(item)

        return GetEventsResponse(items=grouped_events)
