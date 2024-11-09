from fastapi import APIRouter

from app.api.requests.link import JoinByLinkRequest
from app.api.responses.link import JoinByLinkResponse
from app.internal.db.core import SessionDep
from app.internal.services.links import join_by_link


router = APIRouter()


@router.post("/join")
async def join(
    session: SessionDep,
    body: JoinByLinkRequest,
) -> JoinByLinkResponse:
    result = await join_by_link(
        session=session,
        link=body.link,
        user_name=body.user_name,
    )
    return result
