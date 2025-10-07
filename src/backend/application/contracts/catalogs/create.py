from pydantic import BaseModel

from backend.domain.enum.catalog import CatalogVisibility


class CreateCatalogRequest(BaseModel):
    name: str
    parent_id: int | None = None
    visibility: CatalogVisibility = CatalogVisibility.PUBLIC
