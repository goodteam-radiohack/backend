from pydantic import BaseModel


class DeleteCatalogRequest(BaseModel):
    id: int


class DeleteCatalogResponse(BaseModel):
    success: bool
