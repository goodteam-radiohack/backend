from datetime import datetime

from backend.domain.entities.base import BaseEntity
from backend.domain.entities.document import DocumentEntity
from backend.domain.entities.user import UserEntity
from backend.domain.enum.event import EventStatus, EventVisibility


class EventEntity(BaseEntity):
    id: int

    name: str
    description: str

    image: str | None

    scheduled_at: datetime
    ends_at: datetime

    attachments: list[DocumentEntity]

    status: EventStatus

    visibility: EventVisibility
    event_for: UserEntity | None

    def can_set_rsvp(self, user: UserEntity) -> bool:
        return self.visibility == EventVisibility.PUBLIC or self.has_access(user)

    def has_access(self, user: UserEntity) -> bool:
        return bool(
            self.visibility == EventVisibility.PRIVATE
            and self.event_for
            and user.id
            in (
                self.event_for.id,
                self.event_for.helper.id if self.event_for.helper else None,
            )
        )
