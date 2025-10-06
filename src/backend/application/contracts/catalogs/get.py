from pydantic import BaseModel


class GetCatalogRequest(BaseModel):
    id: int
