from typing import Protocol

from backend.domain.dto.catalog import CreateCatalogDTO, UpdateCatalogDTO
from backend.domain.entities.catalog import CatalogEntity


class CatalogReader(Protocol):
    async def with_id(self, catalog_id: int) -> CatalogEntity: ...
    async def get_root(self) -> list[CatalogEntity]: ...


class CatalogWriter(Protocol):
    async def create(self, dto: CreateCatalogDTO) -> CatalogEntity: ...


class CatalogUpdater(Protocol):
    async def update(self, dto: UpdateCatalogDTO) -> CatalogEntity: ...
