from fastapi import APIRouter

from app.api.requests.trip import CreateTripRequest, DeleteTripRequest
from app.api.responses.trip import CreateTripResponse, DeleteTripResponse


router = APIRouter()


@router.post("/new", response_model=CreateTripResponse)
async def new_trip(body: CreateTripRequest) -> CreateTripResponse: ...


@router.get("", response_model=...)
async def get_trip(body: ...) -> ...: ...


@router.delete("", response_model=DeleteTripResponse)
async def delete_trip(body: DeleteTripRequest) -> DeleteTripResponse: ...