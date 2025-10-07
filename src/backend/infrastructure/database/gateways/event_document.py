from dataclasses import dataclass

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.gateways.document import DocumentReader
from backend.application.gateways.event import EventReader
from backend.application.gateways.event_document import EventDocumentWriter
from backend.infrastructure.database.models.associations import event_document


@dataclass
class EventDocumentGateway(EventDocumentWriter):
    session: AsyncSession

    event_reader: EventReader
    document_reader: DocumentReader

    async def attach_document(self, event_id: int, document_id: int) -> None:
        event = await self.event_reader.with_id(event_id)
        document = await self.document_reader.with_id(document_id)

        stmt = insert(event_document).values(event_id=event.id, document_id=document.id)
        await self.session.execute(stmt)

    async def unattach_document(self, event_id: int, document_id: int) -> None:
        event = await self.event_reader.with_id(event_id)
        document = await self.document_reader.with_id(document_id)

        stmt = delete(event_document).where(
            event_document.c.event_id == event.id,
            event_document.c.document_id == document.id,
        )
        await self.session.execute(stmt)
