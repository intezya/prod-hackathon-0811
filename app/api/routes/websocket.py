from fastapi import APIRouter


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: ...) -> ...: ...
