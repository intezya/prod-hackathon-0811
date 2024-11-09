from fastapi import APIRouter


router = APIRouter()


@router.post("/join")
async def join(body: ...) -> ...: ...
