from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.document import DocumentEntity
from backend.infrastructure.database.models.base import BaseModel
from backend.infrastructure.database.models.catalog import CatalogModel
from backend.infrastructure.database.models.user import UserModel


class DocumentModel(BaseModel):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    catalog_id: Mapped[int | None] = mapped_column(
        ForeignKey("catalogs.id"), nullable=True
    )
    catalog: Mapped[CatalogModel] = relationship(back_populates="documents")

    name: Mapped[str] = mapped_column()

    mime: Mapped[str] = mapped_column()
    size: Mapped[int] = mapped_column(BigInteger())

    storage_key: Mapped[str] = mapped_column()
    checksum: Mapped[str] = mapped_column()

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[UserModel] = relationship()

    def to_entity(self) -> DocumentEntity:
        return DocumentEntity.model_validate(self)
