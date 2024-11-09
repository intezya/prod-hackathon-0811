from fastapi import APIRouter

from app.api.requests.event import CreateEvent


router = APIRouter()


@router.post("/new")
# In body we contain is_from_trip and trip_id
async def new_event(body: CreateEvent) -> CreateE: ...


@router.get("")
async def get_event(body: ...) -> ...: ...

