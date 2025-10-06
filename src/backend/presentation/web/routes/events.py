from typing import Annotated, Literal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from backend.application.contracts.events.get import GetEventsRequest, GetEventsResponse
from backend.application.contracts.rsvp.set_status import (
    SetRsvpStatusRequest,
    SetRsvpStatusResponse,
)
from backend.application.usecases.events.get import GetEventsUseCase
from backend.application.usecases.rsvp.set_status import SetRsvpStatusUseCase
from backend.presentation.web.schemas.events import SetRsvpStatusSchema

router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


@router.get("")
async def get_events(
    interactor: FromDishka[GetEventsUseCase],
    period: Annotated[Literal["week"], Query()] = "week",
    offset: Annotated[int, Query()] = 0,
) -> GetEventsResponse:
    return await interactor(GetEventsRequest(period=period, offset=offset))


@router.post("/{event_id}/rsvp")
async def set_rsvp_status(
    event_id: int,
    req: SetRsvpStatusSchema,
    interactor: FromDishka[SetRsvpStatusUseCase],
) -> SetRsvpStatusResponse:
    return await interactor(
        SetRsvpStatusRequest(
            event_id=event_id,
            status=req.status,
            reason=req.reason,
        )
    )
