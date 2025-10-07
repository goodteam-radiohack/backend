from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.catalogs.catalog import CatalogResponse
from backend.application.contracts.catalogs.get_root import (
    GetRootCatalogsRequest,
    GetRootCatalogsResponse,
)
from backend.application.gateways.catalog import CatalogReader


@dataclass
class GetRootCatalogsUseCase(
    Interactor[GetRootCatalogsRequest, GetRootCatalogsResponse]
):
    id_provider: IdProvider

    catalog_reader: CatalogReader

    async def __call__(self, _: GetRootCatalogsRequest) -> GetRootCatalogsResponse:
        user = await self.id_provider.get_user()

        root_catalogs = await self.catalog_reader.get_root(
            user.helping_to_id or user.id
        )
        return GetRootCatalogsResponse(
            catalogs=[CatalogResponse.from_entity(catalog) for catalog in root_catalogs]
        )
