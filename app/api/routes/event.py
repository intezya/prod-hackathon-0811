from app.api.requests.event import (AddDebtorRequest, CreateEventRequest,
                                    GetEventRequest)
from app.api.responses.event import AddDebtorResponse, CreateEventResponse
from app.internal.db.models import EventView
from fastapi import APIRouter

router = APIRouter()


@router.post("/new", response_model=CreateEventResponse)
# In body we contain is_from_trip and trip_id
async def new_event(body: CreateEventRequest) -> CreateEventResponse: ...


@router.post("/add_debtor", response_model=AddDebtorResponse)
async def add_debtor(body: AddDebtorRequest) -> AddDebtorResponse: ...


# TODO: i think need to do like GetEventResponse
@router.get("", response_model=EventView)
async def get_event(body: GetEventRequest) -> EventView: ...
