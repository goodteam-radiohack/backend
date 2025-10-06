from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.auth.logout import LogOutRequest, LogOutResponse
from backend.application.contracts.auth.signin import SignInRequest, SignInResponse
from backend.application.usecases.auth.logout import LogOutUseCase
from backend.application.usecases.auth.signin import SignInUseCase

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/signin")
async def signin(
    req: SignInRequest, interactor: FromDishka[SignInUseCase]
) -> SignInResponse:
    return await interactor(req)


@router.post("/logout")
async def logout(interactor: FromDishka[LogOutUseCase]) -> LogOutResponse:
    return await interactor(LogOutRequest())
