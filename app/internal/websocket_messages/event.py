from app.internal.db.models import EventView, TripView
from app.internal.services.websocket import main_websocket_service as ws_service


async def new_event_in_trip_notify(data: TripView) -> ...:
    context_id = data.id

    for item in data.debts:
        user_websocket = ws_service.get(
            user_name=item.debtor_name,
            id_from_link=context_id,
        )
        if not user_websocket:
            continue
        await user_websocket.send_json(
            {"type": "new-event-in-trip", "data": data.events}
        )


async def new_debtor_in_event_added_notify(
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
            user_name=item.name,
            id_from_link=context_id,
        )
        if not user_websocket:
            continue
        await user_websocket.send_json(
            {"type": "new-debtor-in-event-added", "data": data.debts}
        )
