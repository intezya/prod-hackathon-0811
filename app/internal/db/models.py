import uuid
from typing import List

from sqlmodel import Field, SQLModel


class EventOwner(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str


class Debtor(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    debt: float


class BaseEvent(SQLModel):
    bill_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)

    event_name: str

    debts: List[EventOwner, Debtor, ...] = Field(default_factory=list)


class Trip(SQLModel):
    bill_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_name: str
    event_ids: List[uuid.UUID] = Field(default_factory=list)




class Bills(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_id: ... # TODO

    owner_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)

    name: str
    bill_type: str = "event"

    trips: List[Trip, ...] = Field(default_factory=list)