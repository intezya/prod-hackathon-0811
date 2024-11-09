from app.internal.db.models import TripView
from app.internal.services.websocket import main_websocket_service as ws_service


async def new_event_in_trip(data: TripView):
    context_id = data.id

    for item in data.debts:
        user_websocket = ws_service.get(
            user_name=item.debtor_name,
            id_from_link=context_id,
        )
        if not user_websocket:
            continue
        await user_websocket.send_json({"type": "new-event-in-trip", "data": data})
