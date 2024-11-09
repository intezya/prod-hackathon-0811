# POST /api/event/new
# GET /api/event

import uuid
from typing import List

from app.api.requests.event import CreateEventRequest
from app.internal.db.models import Event, EventView
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_event_by_id(*, session: AsyncSession, id: uuid.UUID) -> Event | None:
    statement = select(Event).where(Event.id == id)
    event = await session.exec(statement)
    return event.first()

async def delete_event_by_id(*, session: AsyncSession, id: uuid.UUID) -> None:
    statement = select(Event).where(Event.id == id)
    event = await session.exec(statement)
    await session.delete(event.first())


async def create_event(
    *, session: AsyncSession, create_event_req: CreateEventRequest
) -> Event:
    if not create_event_req.debts:
        model = Event(
            event_name=create_event_req.event_name,
            owner_name=create_event_req.owner.name,
            owner_description=create_event_req.owner.description,
            debts={},  # type: ignore
        )
    else:
        model = Event(
            event_name=create_event_req.event_name,
            owner_name=create_event_req.owner.name,
            owner_description=create_event_req.owner.description,
            debts=[item.model_dump() for item in create_event_req.debts],  # type: ignore
        )
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


async def get_event_views_from_event_ids(
    *,
    session: AsyncSession,
    event_ids: List[uuid.UUID],
) -> List[EventView]:
    statement = select(Event).where(col(Event.id).in_(event_ids))
    events = await session.exec(statement)
    event_views: List[EventView] = list()
    for event in events:
        event_view = EventView(
            id=event.id, event_name=event.event_name, debts=event.debts
        )
        event_views.append(event_view)
    return event_views
