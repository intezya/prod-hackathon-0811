import uuid

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.requests.event import CreateTripEventRequest
from app.api.requests.trip import CreateTripRequest, DeleteTripRequest, GetTripRequest
from app.api.responses.event import CreateTripEventResponse
from app.api.responses.trip import CreateTripResponse, DeleteTripResponse
from app.internal.config import settings
from app.internal.db.models import TripView
from app.internal.repositories.events import get_event_views_from_event_ids
from app.internal.repositories.links import create_link
from app.internal.repositories.trips import (
    create_trip,
    create_trip_event,
    delete_trip_by_id,
    get_trip_by_id,
)


async def get_trip_view(*, session: AsyncSession, get_trip: GetTripRequest) -> TripView:
    trip_id = uuid.UUID(get_trip.trip_id)
    trip = await get_trip_by_id(session=session, id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    event_views = await get_event_views_from_event_ids(
        session=session, event_ids=trip.event_ids
    )
    trip_view = TripView(id=trip_id, trip_name=trip.trip_name, events=event_views)
    return trip_view


async def create_trip_view(
    *,
    session: AsyncSession,
    create_trip_req: CreateTripRequest,
) -> CreateTripResponse:
    trip = await create_trip(session=session, trip_create=create_trip_req)
    link = await create_link(
        session=session,
        id=trip.id,
        type="trip",
        allowed_names=create_trip_req.allowed_names,
    )
    trip_resp = CreateTripResponse(
        trip_id=str(trip.id),
        link=f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}/link/{link.value}",
    )
    return trip_resp


async def create_trip_event_view(
    *,
    session: AsyncSession,
    create_trip_event_req: CreateTripEventRequest,
) -> CreateTripEventResponse:
    trip_event = await create_trip_event(
        session=session, create_trip_event=create_trip_event_req
    )
    trip_event_resp = CreateTripEventResponse(event_id=str(trip_event.id))
    return trip_event_resp


async def delete_trip(
    *, session: AsyncSession, delete_trip_req: DeleteTripRequest
) -> DeleteTripResponse:
    # only if no events
    trip_id = uuid.UUID(delete_trip_req.trip_id)
    trip = await get_trip_by_id(session=session, id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if trip.event_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await delete_trip_by_id(session=session, id=trip.id)
    return DeleteTripResponse()
