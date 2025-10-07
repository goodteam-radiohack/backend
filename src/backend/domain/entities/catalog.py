from backend.domain.entities.base import BaseEntity
from backend.domain.entities.document import DocumentEntity
from backend.domain.entities.user import UserEntity
from backend.domain.enum.catalog import CatalogVisibility


class OmittedCatalogEntity(BaseEntity):
    id: int
    parent_id: int | None

    name: str

    visibility: CatalogVisibility


class CatalogEntity(BaseEntity):
    id: int
    parent_id: int | None

    name: str

    child: list[OmittedCatalogEntity]
    documents: list[DocumentEntity]

    visibility: CatalogVisibility
    created_by: UserEntity

    def is_author(self, user: UserEntity) -> bool:
        return self.created_by.id != user.id
