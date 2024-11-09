from fastapi import APIRouter

from app.api.requests.event import CreateEventRequest
from app.api.responses.event import CreateEventResponse


router = APIRouter()


@router.post("/new", response_model=CreateEventResponse)
# In body we contain is_from_trip and trip_id
async def new_event(body: CreateEventRequest) -> CreateEventResponse:...


@router.get("")
async def get_event(body: ...) -> ...: ...

