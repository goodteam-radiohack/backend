from dataclasses import dataclass
from datetime import timedelta

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.documents.get import GetDocumentRequest
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.document import DocumentReader
from backend.domain.enum.document import DocumentVisibility
from backend.domain.services.s3 import S3Service

EXPIRES_IN = timedelta(days=7)


@dataclass
class GetDocumentUseCase(Interactor[GetDocumentRequest, DocumentResponse]):
    id_provider: IdProvider

    document_reader: DocumentReader

    s3_service: S3Service

    async def __call__(self, data: GetDocumentRequest) -> DocumentResponse:
        user = await self.id_provider.get_user()

        document = await self.document_reader.with_id(data.id)

        if document.visibility == DocumentVisibility.PRIVATE and not document.is_author(
            user
        ):
            raise UnauthorizedError

        url = await self.s3_service.get_url(document.storage_key, expires_in=EXPIRES_IN)
        return DocumentResponse.from_entity(document, url=url)
