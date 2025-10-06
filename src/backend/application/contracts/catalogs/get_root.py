from pydantic import BaseModel

from backend.application.contracts.catalogs.catalog import CatalogResponse


class GetRootCatalogsRequest(BaseModel):
    pass


class GetRootCatalogsResponse(BaseModel):
    catalogs: list[CatalogResponse]
