from pydantic import BaseModel


class CreateDocumentDTO(BaseModel):
    catalog_id: int | None

    name: str
    mime: str
    size: int

    storage_key: str
    checksum: str

    created_by_id: int
