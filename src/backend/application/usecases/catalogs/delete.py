# backend/application/usecases/catalogs/delete.py
from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.catalogs.delete import (
    DeleteCatalogRequest,
    DeleteCatalogResponse,
)
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.document import DocumentReader, DocumentWriter
from backend.application.gateways.catalog import CatalogReader, CatalogWriter

@dataclass
class DeleteCatalogUseCase(Interactor[DeleteCatalogRequest, DeleteCatalogResponse]):
    id_provider: IdProvider

    catalog_reader: CatalogReader
    catalog_writer: CatalogWriter

    document_reader: DocumentReader
    document_writer: DocumentWriter

    uow: UnitOfWork

    async def __call__(self, data: DeleteCatalogRequest) -> DeleteCatalogResponse:
        user = await self.id_provider.get_user()

        catalog = await self.catalog_reader.with_id(data.id)

        if not catalog.is_author(user):
            raise UnauthorizedError

        documents = await self.document_reader.list_by_catalog(data.id)

        async with self.uow:
            for doc in documents:
                await self.document_writer.delete(doc.id)

            # Удаляем сам каталог
            await self.catalog_writer.delete(data.id)

            await self.uow.commit()

        return DeleteCatalogResponse(success=True)
