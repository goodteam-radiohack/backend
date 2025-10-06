from pydantic import BaseModel


class GetDocumentRequest(BaseModel):
    id: int
