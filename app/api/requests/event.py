from typing import List

from sqlmodel import SQLModel

from app.internal.db.models import Debtor, Owner


class CreateEventRequest(SQLModel):
    event_name: str
    owner: Owner
    debts: List[Debtor]


class CreateTripEventRequest(SQLModel):
    event_name: str
    owner: Owner
    trip_id: str
    debts: List[Debtor]