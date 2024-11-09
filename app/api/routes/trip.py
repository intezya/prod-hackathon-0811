from fastapi import APIRouter

from app.api.requests.trip import CreateTripRequest, DeleteTripRequest, GetTripRequest
from app.api.responses.trip import CreateTripResponse, DeleteTripResponse
from app.internal.db.models import TripView


router = APIRouter()


@router.post("/new", response_model=CreateTripResponse)
async def new_trip(body: CreateTripRequest) -> CreateTripResponse: ...


# Headers: user_name
# TODO: i think need to do like GetTripResponse
@router.get("", response_model=TripView)
async def get_trip(body: GetTripRequest) -> TripView: ...


# Headers: user_name (for check if participate in trip)
# Can be used only if no events
@router.delete("", response_model=DeleteTripResponse)
async def delete_trip(body: DeleteTripRequest) -> DeleteTripResponse: ...
