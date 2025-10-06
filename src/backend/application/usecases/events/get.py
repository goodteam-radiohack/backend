from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from pytz import timezone

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.events.get import GetEventsRequest, GetEventsResponse
from backend.application.gateways.event import EventReader

TZ = timezone("Asia/Yekaterinburg")


@dataclass
class GetEventsUseCase(Interactor[GetEventsRequest, GetEventsResponse]):
    id_provider: IdProvider

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
        await self.id_provider.get_user()

        # TODO: add depute status at every event

        start, end = self._week_range(data.offset)

        events = await self.event_reader.all_window(start, end)
        grouped_events = defaultdict(list)

        for event in events:
            grouped_events[event.scheduled_at.astimezone(tz=TZ).date()].append(event)

        return GetEventsResponse(items=grouped_events)
