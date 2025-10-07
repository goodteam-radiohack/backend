from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.events.attach_document import (
    AttachDocumentRequest,
    UnAttachDocumentRequest,
)
from backend.application.contracts.events.event import EventResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.event import EventReader
from backend.application.gateways.event_document import EventDocumentWriter


@dataclass
class AttachDocumentUseCase(Interactor[AttachDocumentRequest, EventResponse]):
    id_provider: IdProvider

    event_document: EventDocumentWriter
    event_reader: EventReader

    uow: UnitOfWork

    async def __call__(self, data: AttachDocumentRequest) -> EventResponse:
        user = await self.id_provider.get_user()

        event = await self.event_reader.with_id(data.event_id)
        if not event.has_access(user):
            raise UnauthorizedError

        async with self.uow:
            await self.event_document.attach_document(data.event_id, data.document_id)
            await self.uow.commit()

        event = await self.event_reader.with_id(data.event_id)
        return EventResponse.from_entity(event)


@dataclass
class UnAttachDocumentUseCase(Interactor[UnAttachDocumentRequest, EventResponse]):
    id_provider: IdProvider

    event_document: EventDocumentWriter
    event_reader: EventReader

    uow: UnitOfWork

    async def __call__(self, data: UnAttachDocumentRequest) -> EventResponse:
        user = await self.id_provider.get_user()

        event = await self.event_reader.with_id(data.event_id)
        if not event.has_access(user):
            raise UnauthorizedError

        async with self.uow:
            await self.event_document.unattach_document(data.event_id, data.document_id)
            await self.uow.commit()

        event = await self.event_reader.with_id(data.event_id)
        return EventResponse.from_entity(event)
