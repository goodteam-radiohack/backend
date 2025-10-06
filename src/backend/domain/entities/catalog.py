from backend.domain.entities.base import BaseEntity
from backend.domain.entities.document import DocumentEntity


class CatalogEntity(BaseEntity):
    id: int
    parent_id: int

    name: str

    child: list["CatalogEntity"]
    documents: list[DocumentEntity]
