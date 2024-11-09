import uuid
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Debtor(SQLModel):
    name: str
    value: float

class Owner(SQLModel):
    name: str
    description: Optional[str]


class Event(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    owner: Owner
    event_name: str
    debts: List[Debtor, ...] = Field(default_factory=list)
    trip_id: uuid.UUID = Field(nullable=True, default=None)


class Trip(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_name: str
    event_ids: List[uuid.UUID] = Field(default_factory=list)



class Link(SQLModel, table=True):
    value: str = Field(primary_key=True)
    id: uuid.UUID
    type: str
    allowed_user_names: List[str] = Field(default_factory=list)

    @classmethod
    @field_validator("type")
    def validate_link_type(cls, v):
        if v not in ["event", "trip"]:
            raise ValueError("type must be 'event' or 'trip'")
        return v


class EventView(SQLModel):
    id: uuid.UUID
    event_name: str
    debts: List[Debtor, ...]


class TripView(SQLModel):
    id: uuid.UUID
    trip_name: str
    event_ids: List[uuid.UUID]
