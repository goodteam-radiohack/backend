from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.users.me import MeRequest, MeResponse
from backend.application.usecases.users.me import MeUseCase

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/me")
async def me(interactor: FromDishka[MeUseCase]) -> MeResponse:
    return await interactor(MeRequest())
