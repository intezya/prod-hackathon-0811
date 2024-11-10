from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.api.requests.trip import GetTripRequest
from app.api.responses.link import JoinByLinkResponse
from app.internal.repositories.links import get_link_by_value
from app.internal.services.events import get_event_view
from app.internal.services.trips import get_trip_view


async def join_by_link(
    session: AsyncSession, link: str, user_name: str
) -> JoinByLinkResponse:
    link = link.split("/")[-1]
    result = await get_link_by_value(session=session, value=link)
    if user_name not in result.allowed_user_names:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "user not allowed"},
        )
    data = None

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "link not found"},
        )

    if result.type == "event":
        data = await get_event_view(
            session=session,
            event_id=str(result.id),
        )
    elif result.type == "trip":
        data = await get_trip_view(
            session=session,
            get_trip=GetTripRequest(trip_id=str(result.id)),
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "invalid link type"},
        )

    return JoinByLinkResponse(
        context_type=result.type,
        context_id=str(result.id),
        data=data,
    )
