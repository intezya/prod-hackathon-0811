# POST api/trip/new
# GET api/trip
# DELETE api/trip

import uuid

from app.api.requests.trip import CreateTrip
from app.internal.db.models import Trip
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_trip_by_id(*, session: AsyncSession, id: uuid.UUID) -> Trip | None:
     statement = select(Trip).where(Trip.id == id)
     trip = await session.exec(statement)
     return trip.first()

async def delete_trip_by_id(*, session: AsyncSession, id: uuid.UUID) -> None:
     statement = select(Trip).where(Trip.id == id)
     trip = await session.exec(statement)
     await session.delete(trip.first())

async def create_trip(*, session: AsyncSession, trip_create: CreateTrip) -> Trip:
     model = Trip(trip_name=trip_create.name)
     session.add(model)
     await session.commit()
     await session.refresh(model)
     return model
