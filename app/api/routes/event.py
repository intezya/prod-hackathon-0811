from fastapi import APIRouter

from app.api.requests.event import AddDebtorRequest, CreateEventRequest, GetEventRequest
from app.api.responses.event import AddDebtorResponse, CreateEventResponse
from app.internal.db.core import SessionDep
from app.internal.db.models import EventView
from app.internal.services.events import (
    add_debtor_to_event,
    create_event_view,
    get_event_view,
)


router = APIRouter()


@router.post("/new", response_model=CreateEventResponse)
# In body we contain is_from_trip and trip_id
async def new_event(
    body: CreateEventRequest,
    session: SessionDep,
) -> CreateEventResponse:
    result = await create_event_view(session=session, create_event_req=body)
    return result


@router.post("/add_debtor", response_model=AddDebtorResponse)
async def add_debtor(
    body: AddDebtorRequest,
    session: SessionDep,
) -> AddDebtorResponse:
    result = await add_debtor_to_event(session=session, req=body)
    return result


# TODO: i think need to do like GetEventResponse
@router.get("", response_model=EventView)
async def get_event(
    body: GetEventRequest,
    session: SessionDep,
) -> EventView:
    result = await get_event_view(session=session, get_event=body)
    return result
