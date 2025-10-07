from dataclasses import dataclass
from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, with_loader_criteria

from backend.application.gateways.catalog import (
    CatalogReader,
    CatalogUpdater,
    CatalogWriter,
)
from backend.domain.dto.catalog import CreateCatalogDTO, UpdateCatalogDTO
from backend.domain.entities.catalog import CatalogEntity
from backend.domain.enum.catalog import CatalogVisibility
from backend.domain.enum.document import DocumentVisibility
from backend.infrastructure.database.models.catalog import CatalogModel
from backend.infrastructure.database.models.document import DocumentModel
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.catalog import CatalogNotFoundError

_OPTIONS = [
    selectinload(CatalogModel.child),
    selectinload(CatalogModel.documents)
    .joinedload(DocumentModel.created_by)
    .joinedload(UserModel.helper),
    selectinload(CatalogModel.documents)
    .joinedload(DocumentModel.created_by)
    .joinedload(UserModel.helping_to),
    joinedload(CatalogModel.created_by).joinedload(UserModel.helper),
    joinedload(CatalogModel.created_by).joinedload(UserModel.helping_to),
]

# shared queries


@dataclass
class CatalogGateway(CatalogReader, CatalogWriter, CatalogUpdater):
    session: AsyncSession

    @staticmethod
    def _doc_visible(user_id: int | None = None) -> Any:
        return (DocumentModel.visibility == DocumentVisibility.PUBLIC) | (
            (DocumentModel.visibility == DocumentVisibility.PRIVATE)
            & (DocumentModel.created_by_id == user_id)
        )

    async def with_id(
        self, catalog_id: int, user_id: int | None = None
    ) -> CatalogEntity:
        stmt = (
            select(CatalogModel)
            .where(
                CatalogModel.id == catalog_id,
                (CatalogModel.visibility == CatalogVisibility.PUBLIC)
                | (
                    (CatalogModel.visibility == DocumentVisibility.PRIVATE)
                    & (CatalogModel.created_by_id == user_id)
                ),
            )
            .options(
                *_OPTIONS,
                with_loader_criteria(
                    DocumentModel, self._doc_visible(user_id), include_aliases=True
                ),
            )
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise CatalogNotFoundError from exc

        return result.to_entity()

    async def get_root(self, user_id: int | None = None) -> list[CatalogEntity]:
        stmt = (
            select(CatalogModel)
            .where(
                CatalogModel.parent_id.is_(None),
                (CatalogModel.visibility == CatalogVisibility.PUBLIC)
                | (
                    (CatalogModel.visibility == DocumentVisibility.PRIVATE)
                    & (CatalogModel.created_by_id == user_id)
                ),
            )
            .options(
                *_OPTIONS,
                with_loader_criteria(
                    DocumentModel, self._doc_visible(user_id), include_aliases=True
                ),
            )
        )

        results = (await self.session.scalars(stmt)).all()
        return [result.to_entity() for result in results]

    async def create(self, dto: CreateCatalogDTO, user_id: int) -> CatalogEntity:
        stmt = (
            insert(CatalogModel).values(**dto.model_dump()).returning(CatalogModel.id)
        )

        catalog_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(catalog_id, user_id)

    async def update(self, dto: UpdateCatalogDTO) -> CatalogEntity:
        stmt = (
            update(CatalogModel)
            .values(**dto.model_dump(exclude={"id"}, exclude_unset=True))
            .where(CatalogModel.id == dto.id)
        )

        await self.session.execute(stmt)

        return await self.with_id(dto.id)

    async def delete(self, catalog_id: int) -> None:
        stmt = delete(CatalogModel).where(CatalogModel.id == catalog_id)
        await self.session.execute(stmt)
