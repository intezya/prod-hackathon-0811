from typing import List, Optional

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


class GetEventRequest(SQLModel):
    event_id: str


class AddDebtorRequest(SQLModel):
    event_id: str
    debtor_name: str
    debtor_value: float
    context_id: Optional[str]
