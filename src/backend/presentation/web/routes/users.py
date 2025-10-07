from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Query

from backend.application.contracts.users.create import CreateUserRequest
from backend.application.contracts.users.get import GetUsersRequest, GetUsersResponse
from backend.application.contracts.users.me import GetMeRequest, GetMeResponse
from backend.application.contracts.users.user import UserResponse
from backend.application.usecases.users.create import CreateUserUseCase
from backend.application.usecases.users.get import GetUsersUseCase
from backend.application.usecases.users.me import GetMeUseCase
from backend.presentation.web.dependencies.authorization import authorization_header

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
    dependencies=[Depends(authorization_header)],
)


@router.get("/me")
async def get_me(interactor: FromDishka[GetMeUseCase]) -> GetMeResponse:
    return await interactor(GetMeRequest())


@router.get("")
async def get_users(
    interactor: FromDishka[GetUsersUseCase],
    limit: Annotated[int, Query(gt=0)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> GetUsersResponse:
    return await interactor(GetUsersRequest(limit=limit, offset=offset))


@router.post("")
async def create_user(
    req: CreateUserRequest, interactor: FromDishka[CreateUserUseCase]
) -> UserResponse:
    return await interactor(req)
