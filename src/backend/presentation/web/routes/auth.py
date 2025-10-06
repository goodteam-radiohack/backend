from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.auth.signin import SignInRequest, SignInResponse
from backend.application.usecases.auth.signin import SignInUseCase

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/signin")
async def signin(
    req: SignInRequest, interactor: FromDishka[SignInUseCase]
) -> SignInResponse:
    return await interactor(req)
