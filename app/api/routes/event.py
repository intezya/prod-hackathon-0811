from fastapi import APIRouter

from app.api.requests.event import CreateEventRequest, GetEventRequest
from app.api.responses.event import CreateEventResponse
from app.internal.db.models import EventView


router = APIRouter()


@router.post("/new", response_model=CreateEventResponse)
# In body we contain is_from_trip and trip_id
async def new_event(body: CreateEventRequest) -> CreateEventResponse:...


# TODO: i think need to do like GetEventResponse
@router.get("", response_model=EventView)
async def get_event(body: GetEventRequest) -> EventView: ...

