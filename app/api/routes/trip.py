from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.requests.trip import CreateTripRequest, DeleteTripRequest, GetTripRequest
from app.api.responses.trip import CreateTripResponse, DeleteTripResponse
from app.internal.db.core import get_db
from app.internal.db.models import TripView
from app.internal.services.trips import get_trip_view


router = APIRouter()


@router.post("/new", response_model=CreateTripResponse)
async def new_trip(body: CreateTripRequest) -> CreateTripResponse: ...


# TODO: i think need to do like GetTripResponse
@router.get("", response_model=TripView)
async def get_trip(
    body: GetTripRequest,
    session: AsyncSession = get_db(),
) -> TripView:
    result = await get_trip_view(session=session, get_trip=body)
    return result


# Can be used only if no events
@router.delete("", response_model=DeleteTripResponse)
async def delete_trip(body: DeleteTripRequest) -> DeleteTripResponse: ...
