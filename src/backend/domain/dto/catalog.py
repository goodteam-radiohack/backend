from pydantic import BaseModel


class CreateCatalogDTO(BaseModel):
    name: str
    parent_id: int | None


class UpdateCatalogDTO(BaseModel):
    id: int

    name: str | None = None
    parent_id: int | None = None
