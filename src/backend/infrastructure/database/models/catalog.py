from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.catalog import CatalogEntity
from backend.domain.enum.catalog import CatalogVisibility
from backend.infrastructure.database.models.base import BaseModel
from backend.infrastructure.database.models.user import UserModel

if TYPE_CHECKING:
    from backend.infrastructure.database.models.document import DocumentModel


class CatalogModel(BaseModel):
    __tablename__ = "catalogs"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("catalogs.id", ondelete="SET NULL"), nullable=True
    )
    parent: Mapped["CatalogModel"] = relationship(
        lambda: CatalogModel,
        back_populates="child",
        remote_side=lambda: CatalogModel.id,
    )

    child: Mapped[list["CatalogModel"]] = relationship(
        lambda: CatalogModel,
        back_populates="parent",
        foreign_keys=lambda: CatalogModel.parent_id,
        cascade="all, delete-orphan",
    )
    documents: Mapped[list["DocumentModel"]] = relationship()

    visibility: Mapped[CatalogVisibility] = mapped_column(
        ENUM(CatalogVisibility, name="catalog_visibility"),
        server_default="PUBLIC",
        default=CatalogVisibility.PUBLIC,
    )

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[UserModel] = relationship()

    __table_args__ = (UniqueConstraint(parent_id, name, name="uq_catalog_parent_name"),)

    def to_entity(self) -> CatalogEntity:
        return CatalogEntity.model_validate(self)
