from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.documents.delete import (
    DeleteDocumentRequest,
    DeleteDocumentResponse,
)
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.document import DocumentReader, DocumentWriter
from backend.domain.enum.user import UserRole
from backend.domain.services.s3 import S3Service


@dataclass
class DeleteDocumentUseCase(Interactor[DeleteDocumentRequest, DeleteDocumentResponse]):
    id_provider: IdProvider

    document_reader: DocumentReader
    document_writer: DocumentWriter

    s3_service: S3Service

    uow: UnitOfWork

    async def __call__(self, data: DeleteDocumentRequest) -> DeleteDocumentResponse:
        user = await self.id_provider.get_user()
        document = await self.document_reader.with_id(data.id)

        if not user.role == UserRole.ADMIN and not document.is_author(user):
            raise UnauthorizedError

        await self.s3_service.delete(document.storage_key)

        async with self.uow:
            await self.document_writer.delete(data.id)
            await self.uow.commit()

        return DeleteDocumentResponse(success=True)
