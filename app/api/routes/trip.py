from fastapi import APIRouter

from app.api.requests.event import CreateTripEventRequest
from app.api.requests.trip import CreateTripRequest, DeleteTripRequest, GetTripRequest
from app.api.responses.event import CreateTripEventResponse
from app.api.responses.trip import CreateTripResponse, DeleteTripResponse
from app.internal.db.core import SessionDep
from app.internal.db.models import TripView
from app.internal.services.trips import (
    create_trip_event_view,
    create_trip_view,
    get_trip_view,
)


router = APIRouter()


@router.post("/new", response_model=CreateTripResponse)
async def new_trip(session: SessionDep, body: CreateTripRequest) -> CreateTripResponse:
    result = await create_trip_view(session=session, create_trip_req=body)
    return result


@router.post("/event/new", response_model=CreateTripEventResponse)
async def new_trip_event(
    session: SessionDep,
    body: CreateTripEventRequest,
) -> CreateTripEventResponse:
    result = await create_trip_event_view(session=session, create_trip_event_req=body)
    return result


# TODO: i think need to do like GetTripResponse
@router.get("/{trip_id}", response_model=TripView)
async def get_trip(
    session: SessionDep,
    trip_id: str,
) -> TripView:
    body = GetTripRequest(trip_id=trip_id)
    result = await get_trip_view(session=session, get_trip=body)
    return result


# Can be used only if no events
@router.delete("", response_model=DeleteTripResponse)
async def delete_trip(body: DeleteTripRequest) -> DeleteTripResponse: ...
