from uuid import UUID

from pydantic import BaseModel


class UploadDocumentRequest(BaseModel):
    ticket: UUID
    body: bytes
