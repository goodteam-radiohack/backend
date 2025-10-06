from pydantic import BaseModel

from backend.domain.enum.document import DocumentVisibility


class TicketEntity(BaseModel):
    catalog_id: int | None
    name: str
    visibility: DocumentVisibility
    user_id: int
