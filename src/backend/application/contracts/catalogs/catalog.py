from pydantic import BaseModel

from backend.application.contracts.documents.document import DocumentResponse
from backend.domain.entities.catalog import CatalogEntity, OmittedCatalogEntity


class OmittedCatalogResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, entity: OmittedCatalogEntity) -> "OmittedCatalogResponse":
        return OmittedCatalogResponse(
            id=entity.id,
            name=entity.name,
        )


class CatalogResponse(BaseModel):
    id: int
    name: str

    parent_id: int | None

    child: list[OmittedCatalogResponse]
    documents: list[DocumentResponse]

    @classmethod
    def from_entity(cls, entity: CatalogEntity) -> "CatalogResponse":
        return CatalogResponse(
            id=entity.id,
            name=entity.name,
            parent_id=entity.parent_id,
            child=[
                OmittedCatalogResponse(id=item.id, name=item.name)
                for item in entity.child
            ],
            documents=[DocumentResponse.from_entity(item) for item in entity.documents],
        )
