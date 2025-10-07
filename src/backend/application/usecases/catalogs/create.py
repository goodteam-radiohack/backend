from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.catalogs.catalog import CatalogResponse
from backend.application.contracts.catalogs.create import CreateCatalogRequest
from backend.application.gateways.catalog import CatalogReader, CatalogWriter
from backend.domain.dto.catalog import CreateCatalogDTO


@dataclass
class CreateCatalogUseCase(Interactor[CreateCatalogRequest, CatalogResponse]):
    id_provider: IdProvider

    catalog_reader: CatalogReader
    catalog_writer: CatalogWriter

    uow: UnitOfWork

    async def __call__(self, data: CreateCatalogRequest) -> CatalogResponse:
        user = await self.id_provider.get_user()

        if data.parent_id:
            # TODO: replace with `exists` query
            await self.catalog_reader.with_id(data.parent_id)

        async with self.uow:
            catalog = await self.catalog_writer.create(
                CreateCatalogDTO(
                    name=data.name,
                    parent_id=data.parent_id,
                    visibility=data.visibility,
                    created_by_id=user.id,
                )
            )

            await self.uow.commit()

        return CatalogResponse.from_entity(catalog)
