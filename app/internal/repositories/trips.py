# POST api/trip/new
# GET api/trip
# DELETE api/trip
# POST /api/trip/event/new

import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.requests.event import CreateTripEventRequest
from app.api.requests.trip import CreateTripRequest
from app.internal.db.models import Event, Trip


async def get_trip_by_id(*, session: AsyncSession, id: uuid.UUID) -> Trip | None:
    statement = select(Trip).where(Trip.id == id)
    trip = await session.exec(statement)
    return trip.first()


async def delete_trip_by_id(*, session: AsyncSession, id: uuid.UUID) -> None:
    statement = select(Trip).where(Trip.id == id)
    trip = await session.exec(statement)
    await session.delete(trip.first())


async def create_trip(*, session: AsyncSession, trip_create: CreateTripRequest) -> Trip:
    model = Trip(trip_name=trip_create.name)
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model.model_copy()


async def create_trip_event(
    *, session: AsyncSession, create_trip_event: CreateTripEventRequest
) -> Event:
    model = Event(
        event_name=create_trip_event.event_name,
        owner_name=create_trip_event.owner.name,
        owner_description=create_trip_event.owner.description,
        debts=[item.model_dump() for item in create_trip_event.debts],
    )
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model
