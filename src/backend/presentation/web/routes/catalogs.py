from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.catalogs.catalog import CatalogResponse
from backend.application.contracts.catalogs.get import GetCatalogRequest
from backend.application.contracts.catalogs.get_root import (
    GetRootCatalogsRequest,
    GetRootCatalogsResponse,
)
from backend.application.usecases.catalogs.get import GetCatalogUseCase
from backend.application.usecases.catalogs.get_root import GetRootCatalogsUseCase

router = APIRouter(prefix="/catalogs", tags=["Catalogs"], route_class=DishkaRoute)


@router.get("")
async def get_root_catalogs(
    interactor: FromDishka[GetRootCatalogsUseCase],
) -> GetRootCatalogsResponse:
    return await interactor(GetRootCatalogsRequest())


@router.get("/{catalog_id}")
async def get_catalog_by_id(
    catalog_id: int, interactor: FromDishka[GetCatalogUseCase]
) -> CatalogResponse:
    return await interactor(GetCatalogRequest(id=catalog_id))
