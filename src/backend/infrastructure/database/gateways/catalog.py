from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.application.gateways.catalog import (
    CatalogReader,
    CatalogUpdater,
    CatalogWriter,
)
from backend.domain.dto.catalog import CreateCatalogDTO, UpdateCatalogDTO
from backend.domain.entities.catalog import CatalogEntity
from backend.infrastructure.database.models.catalog import CatalogModel
from backend.infrastructure.errors.gateways.catalog import CatalogNotFoundError

_OPTIONS = [selectinload(CatalogModel.child), selectinload(CatalogModel.documents)]


@dataclass
class CatalogGateway(CatalogReader, CatalogWriter, CatalogUpdater):
    session: AsyncSession

    async def with_id(self, catalog_id: int) -> CatalogEntity:
        stmt = (
            select(CatalogModel).where(CatalogModel.id == catalog_id).options(*_OPTIONS)
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise CatalogNotFoundError from exc

        return result.to_entity()

    async def get_root(self) -> list[CatalogEntity]:
        stmt = (
            select(CatalogModel)
            .where(CatalogModel.parent_id.is_(None))
            .options(*_OPTIONS)
        )

        results = (await self.session.scalars(stmt)).all()
        return [result.to_entity() for result in results]

    async def create(self, dto: CreateCatalogDTO) -> CatalogEntity:
        stmt = (
            insert(CatalogModel).values(**dto.model_dump()).returning(CatalogModel.id)
        )

        catalog_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(catalog_id)

    async def update(self, dto: UpdateCatalogDTO) -> CatalogEntity:
        stmt = (
            update(CatalogModel)
            .values(**dto.model_dump(exclude={"id"}, exclude_unset=True))
            .where(CatalogModel.id == dto.id)
        )

        await self.session.execute(stmt)

        return await self.with_id(dto.id)
