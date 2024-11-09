from fastapi import APIRouter

from app.api.requests.link import JoinByLinkRequest
from app.api.responses.link import JoinByLinkResponse


router = APIRouter()


@router.post("/join")
async def join(body: JoinByLinkRequest) -> JoinByLinkResponse: ...
