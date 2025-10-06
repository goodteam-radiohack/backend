from backend.domain.entities.base import BaseEntity
from backend.domain.entities.document import DocumentEntity


class OmittedCatalogEntity(BaseEntity):
    id: int
    parent_id: int | None

    name: str


class CatalogEntity(BaseEntity):
    id: int
    parent_id: int | None

    name: str

    child: list[OmittedCatalogEntity]
    documents: list[DocumentEntity]
