from pydantic import BaseModel


class AttachDocumentRequest(BaseModel):
    event_id: int
    document_id: int


class UnAttachDocumentRequest(BaseModel):
    event_id: int
    document_id: int
