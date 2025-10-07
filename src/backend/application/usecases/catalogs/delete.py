from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.catalogs.delete import (
    DeleteCatalogRequest,
    DeleteCatalogResponse,
)
from backend.application.errors.access import UnauthorizedError
from backend.application.errors.catalog import CatalogNotEmptyError
from backend.application.gateways.catalog import CatalogReader, CatalogWriter
from backend.domain.enum.user import UserRole


@dataclass
class DeleteCatalogUseCase(Interactor[DeleteCatalogRequest, DeleteCatalogResponse]):
    id_provider: IdProvider

    catalog_reader: CatalogReader
    catalog_writer: CatalogWriter

    uow: UnitOfWork

    async def __call__(self, data: DeleteCatalogRequest) -> DeleteCatalogResponse:
        user = await self.id_provider.get_user()

        catalog = await self.catalog_reader.with_id(data.id)

        if user.role != UserRole.ADMIN and not catalog.is_author(user):
            raise UnauthorizedError

        if len(catalog.child) > 0 or len(catalog.documents) > 0:
            raise CatalogNotEmptyError

        async with self.uow:
            await self.catalog_writer.delete(catalog.id)
            await self.uow.commit()

        return DeleteCatalogResponse(success=True)
