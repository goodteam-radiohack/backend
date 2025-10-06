from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.documents.get import GetDocumentRequest
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.document import DocumentReader
from backend.domain.enum.document import DocumentVisibility


@dataclass
class GetDocumentUseCase(Interactor[GetDocumentRequest, DocumentResponse]):
    id_provider: IdProvider

    document_reader: DocumentReader

    async def __call__(self, data: GetDocumentRequest) -> DocumentResponse:
        user = await self.id_provider.get_user()

        document = await self.document_reader.with_id(data.id)

        if document.visibility == DocumentVisibility.PRIVATE and not document.is_author(
            user
        ):
            raise UnauthorizedError

        return DocumentResponse.from_entity(document)
