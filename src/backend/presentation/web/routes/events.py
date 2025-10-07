from typing import Annotated, Literal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Query

from backend.application.contracts.events.attach_document import (
    AttachDocumentRequest,
    UnAttachDocumentRequest,
)
from backend.application.contracts.events.create import (
    CreateEventRequest,
    OmittedUpdateEventRequest,
    UpdateEventRequest,
)
from backend.application.contracts.events.event import EventResponse
from backend.application.contracts.events.get import GetEventsRequest, GetEventsResponse
from backend.application.contracts.rsvp.set_status import (
    SetRsvpStatusRequest,
    SetRsvpStatusResponse,
)
from backend.application.usecases.events.attach_document import (
    AttachDocumentUseCase,
    UnAttachDocumentUseCase,
)
from backend.application.usecases.events.create import CreateEventUseCase
from backend.application.usecases.events.get import GetEventsUseCase
from backend.application.usecases.events.update import UpdateEventUseCase
from backend.application.usecases.rsvp.set_status import SetRsvpStatusUseCase
from backend.presentation.web.dependencies.authorization import authorization_header
from backend.presentation.web.schemas.events import SetRsvpStatusSchema

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    route_class=DishkaRoute,
    dependencies=[Depends(authorization_header)],
)


@router.get("")
async def get_events(
    interactor: FromDishka[GetEventsUseCase],
    period: Annotated[Literal["week"], Query()] = "week",
    offset: Annotated[int, Query()] = 0,
) -> GetEventsResponse:
    return await interactor(GetEventsRequest(period=period, offset=offset))


@router.post("")
async def create_event(
    req: CreateEventRequest, interactor: FromDishka[CreateEventUseCase]
) -> EventResponse:
    return await interactor(req)


@router.patch("/{event_id}")
async def update_event(
    event_id: int,
    req: OmittedUpdateEventRequest,
    interactor: FromDishka[UpdateEventUseCase],
) -> EventResponse:
    return await interactor(
        UpdateEventRequest(
            id=event_id,
            **req.model_dump(exclude_unset=True),
        )
    )


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
            reason_document_id=req.reason_document_id,
        )
    )


@router.post("/{event_id}/attach")
async def attach_document(
    event_id: int,
    document_id: int,
    interactor: FromDishka[AttachDocumentUseCase],
) -> EventResponse:
    return await interactor(
        AttachDocumentRequest(
            event_id=event_id,
            document_id=document_id,
        )
    )


@router.delete("/{event_id}/attach")
async def unattach_document(
    event_id: int,
    document_id: int,
    interactor: FromDishka[UnAttachDocumentUseCase],
) -> EventResponse:
    return await interactor(
        UnAttachDocumentRequest(
            event_id=event_id,
            document_id=document_id,
        )
    )
