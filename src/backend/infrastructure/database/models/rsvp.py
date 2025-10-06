from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.rsvp import RSVPEntity
from backend.domain.enum.rsvp import RSVPStatus
from backend.infrastructure.database.models.base import BaseModel
from backend.infrastructure.database.models.document import DocumentModel


class RSVPModel(BaseModel):
    __tablename__ = "events_rsvp"

    id: Mapped[int] = mapped_column(primary_key=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[RSVPStatus] = mapped_column(ENUM(RSVPStatus, name="rsvp_statuses"))

    reason: Mapped[str | None] = mapped_column(nullable=True)

    reason_document_id: Mapped[int | None] = mapped_column(
        ForeignKey("documents.id"), nullable=True
    )
    reason_document: Mapped[DocumentModel | None] = relationship()

    __table_args__ = (UniqueConstraint(event_id, user_id),)

    def to_entity(self) -> RSVPEntity:
        return RSVPEntity.model_validate(self)
