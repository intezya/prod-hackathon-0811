from typing import List

from sqlmodel import SQLModel

from app.internal.db.models import Debtor


class CreateEventRequest(SQLModel):
    event_name: str
    owner_name: str
    debts: List[Debtor]


class CreateTripEventRequest(SQLModel):
    event_name: str
    owner_name: str
    trip_id: str
    debts: List[Debtor]