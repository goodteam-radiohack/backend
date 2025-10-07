from pydantic import BaseModel

from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.users.user import UserResponse
from backend.domain.entities.catalog import CatalogEntity, OmittedCatalogEntity
from backend.domain.enum.catalog import CatalogVisibility


class OmittedCatalogResponse(BaseModel):
    id: int
    name: str

    visibility: CatalogVisibility

    @classmethod
    def from_entity(cls, entity: OmittedCatalogEntity) -> "OmittedCatalogResponse":
        return OmittedCatalogResponse(
            id=entity.id,
            name=entity.name,
            visibility=entity.visibility,
        )


class CatalogResponse(BaseModel):
    id: int
    name: str

    parent_id: int | None

    child: list[OmittedCatalogResponse]
    documents: list[DocumentResponse]

    visibility: CatalogVisibility
    created_by: UserResponse

    @classmethod
    def from_entity(cls, entity: CatalogEntity) -> "CatalogResponse":
        return CatalogResponse(
            id=entity.id,
            name=entity.name,
            parent_id=entity.parent_id,
            child=[OmittedCatalogResponse.from_entity(item) for item in entity.child],
            documents=[DocumentResponse.from_entity(item) for item in entity.documents],
            visibility=entity.visibility,
            created_by=UserResponse.from_entity(entity.created_by),
        )
