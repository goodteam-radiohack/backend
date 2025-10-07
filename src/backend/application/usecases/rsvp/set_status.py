from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.rsvp.set_status import (
    SetRsvpStatusRequest,
    SetRsvpStatusResponse,
)
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.document import DocumentReader
from backend.application.gateways.event import EventReader
from backend.application.gateways.rsvp import RsvpReader, RsvpWriter
from backend.domain.dto.rsvp import CreateRsvpDTO
from backend.domain.enum.document import DocumentVisibility
from backend.infrastructure.errors.gateways.event import EventNotFoundError
from backend.infrastructure.errors.gateways.rsvp import RsvpNotFoundError


@dataclass
class SetRsvpStatusUseCase(Interactor[SetRsvpStatusRequest, SetRsvpStatusResponse]):
    id_provider: IdProvider

    document_reader: DocumentReader
    event_reader: EventReader

    rsvp_reader: RsvpReader
    rsvp_writer: RsvpWriter

    uow: UnitOfWork

    async def __call__(self, data: SetRsvpStatusRequest) -> SetRsvpStatusResponse:
        user = await self.id_provider.get_user()

        if not await self.event_reader.exists(data.event_id):
            raise EventNotFoundError

        if data.reason_document_id:
            document = await self.document_reader.with_id(data.reason_document_id)

            if (
                document.visibility == DocumentVisibility.PRIVATE
                and not document.is_author(user)
            ):
                raise UnauthorizedError(
                    "Unauthorized (document is private and uploaded by another user)"
                )

        async with self.uow:
            try:
                rsvp = await self.rsvp_reader.with_user_and_event(
                    user.id, data.event_id
                )
                await self.rsvp_writer.delete(rsvp.id)
            except RsvpNotFoundError:
                pass

            rsvp = await self.rsvp_writer.create(
                CreateRsvpDTO(
                    event_id=data.event_id,
                    user_id=user.id,
                    status=data.status,
                    reason=data.reason,
                    reason_document_id=data.reason_document_id,
                )
            )

            await self.uow.commit()

        return SetRsvpStatusResponse(success=True)
