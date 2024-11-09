from typing import List, Optional

from app.internal.db.models import Debtor, Owner
from sqlmodel import SQLModel


class CreateEventRequest(SQLModel):
    event_name: str
    owner: Owner
    debts: List[Debtor]


class CreateTripEventRequest(SQLModel):
    event_name: str
    owner: Owner
    trip_id: str
    debts: List[Debtor]


class GetEventRequest(SQLModel):
    event_id: str
