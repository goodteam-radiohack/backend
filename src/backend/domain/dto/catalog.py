from pydantic import BaseModel

from backend.domain.enum.catalog import CatalogVisibility


class CreateCatalogDTO(BaseModel):
    name: str
    parent_id: int | None

    visibility: CatalogVisibility
    created_by_id: int


class UpdateCatalogDTO(BaseModel):
    id: int

    name: str | None = None
    parent_id: int | None = None

    visibility: CatalogVisibility | None = None
