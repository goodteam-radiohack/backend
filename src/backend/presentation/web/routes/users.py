from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.users.me import GetMeRequest, GetMeResponse
from backend.application.usecases.users.me import GetMeUseCase

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/me")
async def get_me(interactor: FromDishka[GetMeUseCase]) -> GetMeResponse:
    return await interactor(GetMeRequest())
