import uuid

from app.api.requests.event import CreateEventRequest, GetEventRequest
from app.api.responses.event import CreateEventResponse
from app.internal.config import settings
from app.internal.db.models import EventView
from app.internal.repositories.events import create_event, get_event_by_id
from app.internal.repositories.links import create_link
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_event_view(*, session: AsyncSession, get_event: GetEventRequest) -> EventView:
    event_id = uuid.UUID(get_event.event_id)
    event = await get_event_by_id(session=session, id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    event_view = EventView(id=event.id, event_name=event.event_name, debts=event.debts)
    return event_view

async def create_event_view(*, session: AsyncSession, create_event_req: CreateEventRequest) -> CreateEventResponse:
    # create event -> link by id
    event = await create_event(session=session, create_event_req=create_event_req)
    link = await create_link(session=session, id=event.id, type="event")
    event_resp = CreateEventResponse(event_id=str(event.id), link=f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}/link/{link.value}")
    return event_resp
