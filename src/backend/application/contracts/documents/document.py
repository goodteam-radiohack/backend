from pydantic import BaseModel

from backend.application.contracts.users.user import UserResponse
from backend.domain.entities.document import DocumentEntity


class DocumentResponse(BaseModel):
    id: int

    catalog_id: int | None

    name: str
    mime: str
    size: int

    url: str

    created_by: UserResponse

    @classmethod
    def from_entity(cls, entity: DocumentEntity) -> "DocumentResponse":
        return DocumentResponse(
            id=entity.id,
            catalog_id=entity.catalog_id,
            name=entity.name,
            mime=entity.mime,
            size=entity.size,
            url="https://google.com",  # TODO: change to pre-signed S3
            created_by=UserResponse.from_entity(entity.created_by),
        )
