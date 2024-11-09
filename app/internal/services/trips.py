import uuid

from app.api.requests.trip import GetTripRequest
from app.api.responses.trip import CreateTripResponse
from app.internal.config import settings
from app.internal.db.models import TripView
from app.internal.repositories.events import get_event_views_from_event_ids
from app.internal.repositories.trips import get_trip_by_id
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_trip_view(*, session: AsyncSession, get_trip: GetTripRequest) -> TripView:
    trip_id = uuid.UUID(get_trip.trip_id)
    trip = await get_trip_by_id(session=session, id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    event_views = await get_event_views_from_event_ids(session=session, event_ids=trip.event_ids)
    trip_view = TripView(id=trip_id, trip_name=trip.trip_name,events=event_views)
    return trip_view
