from typing import Annotated, Literal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from backend.application.contracts.events.get import GetEventsRequest, GetEventsResponse
from backend.application.usecases.events.get import GetEventsUseCase

router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


@router.get("")
async def get_events(
    interactor: FromDishka[GetEventsUseCase],
    period: Annotated[Literal["week"], Query()] = "week",
    offset: Annotated[int, Query()] = 0,
) -> GetEventsResponse:
    return await interactor(GetEventsRequest(period=period, offset=offset))
