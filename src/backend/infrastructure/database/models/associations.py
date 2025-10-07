from sqlalchemy import Column, ForeignKey, Table

from backend.infrastructure.database.models.base import BaseModel

event_document = Table(
    "event_document",
    BaseModel.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("document_id", ForeignKey("documents.id"), primary_key=True),
)
