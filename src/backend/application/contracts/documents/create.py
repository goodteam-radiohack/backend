from uuid import UUID

from pydantic import BaseModel

from backend.domain.enum.document import DocumentVisibility


class CreateDocumentRequest(BaseModel):
    catalog_id: int | None = None
    name: str
    visibility: DocumentVisibility = DocumentVisibility.PUBLIC


class CreateDocumentResponse(BaseModel):
    success: bool
    ticket: UUID
