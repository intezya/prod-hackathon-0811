# POST /api/event/new
# GET /api/event

import uuid

from app.api.requests.event import CreateEventRequest
from app.internal.db.models import Event
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_event_by_id(*, session: AsyncSession, id: uuid.UUID) -> Event | None:
    statement = select(Event).where(Event.id == id)
    event = await session.exec(statement)
    return event.first()

async def create_event(*, session: AsyncSession, create_event: CreateEventRequest) -> Event:
    model = Event(event_name=create_event.event_name, owner=create_event.owner, debts=create_event.debts)
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model
