from fastapi import APIRouter, WebSocket

from app.api.requests.websocket import ConnectMainWebsocketRequest
from app.internal.services.websocket import main_websocket_service as ws_service


router = APIRouter()


@router.websocket_route("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    body: ConnectMainWebsocketRequest,
) -> ...:
    await ws_service.connect(
        websocket,
        body.user_name,
        body.id_from_link,
    )
