from fastapi import APIRouter


router = APIRouter()


@router.post("/new")
# In body we contain is_from_trip and trip_id
async def new_event(body: ...) -> ...: ...


@router.get("")
async def get_event(body: ...) -> ...: ...

