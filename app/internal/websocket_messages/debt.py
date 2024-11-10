from typing import Optional

from app.internal.db.models import EventView
from app.internal.services.websocket import main_websocket_service as ws_service


async def debt_paid_out_notify(
    data: EventView,
    context_id: Optional[str],  # Need to set only if event is in trip
) -> ...:
    """
    PLS SET CONTEXT_ID IF EVENT IS IN TRIP
    """
    if context_id is None:
        context_id = data.id  # If event is separated (not in trip)

    for item in data.debts:
        user_websocket = ws_service.get(
            user_name=item.debtor_name,
            id_from_link=context_id,
        )
        if not user_websocket:
            continue
        await user_websocket.send_json({"type": "debt-paid-out", "data": data})


async def debt_forgiven_notify(
    data: EventView,
    context_id: str,  # Need to set only if event is in trip
) -> ...:
    """
    PLS SET CONTEXT_ID IF EVENT IS IN TRIP
    """
    if context_id is None:
        context_id = data.id  # If event is separated (not in trip)

    for item in data.debts:
        user_websocket = ws_service.get(
            user_name=item.debtor_name,
            id_from_link=context_id,
        )
        if not user_websocket:
            continue
        await user_websocket.send_json({"type": "debt-forgiven", "data": data})
