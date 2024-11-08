import uuid
from typing import List

from sqlmodel import Field, SQLModel



class Debtor(SQLModel):
    name: str
    debt: float


class BaseEvent(SQLModel):
    bill_id: uuid.UUID = Field(primary_key=True, nullable=False)
    owner_name: str

    event_name: str

    debts: List[Debtor, ...] = Field(default_factory=list)


class Trip(SQLModel):
    bill_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_name: str
    event_ids: List[uuid.UUID] = Field(default_factory=list)


class Bills(SQLModel):
    bill_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_name: str
    bill_type: str = "event"
    users: List[uuid.UUID] = Field(default_factory=list)
