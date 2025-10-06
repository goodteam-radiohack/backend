from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.documents.create import (
    CreateDocumentRequest,
    CreateDocumentResponse,
)
from backend.domain.entities.ticket import TicketEntity
from backend.infrastructure.errors.cache.ticket import DocumentTicketGateway


@dataclass
class CreateDocumentUseCase(Interactor[CreateDocumentRequest, CreateDocumentResponse]):
    id_provider: IdProvider
    ticket: DocumentTicketGateway

    async def __call__(self, data: CreateDocumentRequest) -> CreateDocumentResponse:
        user = await self.id_provider.get_user()

        ticket = await self.ticket.save(
            TicketEntity(
                catalog_id=data.catalog_id,
                name=data.name,
                visibility=data.visibility,
                user_id=user.id,
            )
        )

        return CreateDocumentResponse(success=True, ticket=ticket)
