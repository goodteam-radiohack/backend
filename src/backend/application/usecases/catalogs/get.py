from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.catalogs.catalog import CatalogResponse
from backend.application.contracts.catalogs.get import GetCatalogRequest
from backend.application.gateways.catalog import CatalogReader


@dataclass
class GetCatalogUseCase(Interactor[GetCatalogRequest, CatalogResponse]):
    id_provider: IdProvider

    catalog_reader: CatalogReader

    async def __call__(self, data: GetCatalogRequest) -> CatalogResponse:
        await self.id_provider.get_user()

        catalog = await self.catalog_reader.with_id(data.id)
        return CatalogResponse.from_entity(catalog)
