from pydantic import BaseModel


class DeleteDocumentRequest(BaseModel):
    id: int


class DeleteDocumentResponse(BaseModel):
    success: bool
