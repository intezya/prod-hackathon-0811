import uuid
from typing import List

from pydantic import field_validator
from sqlmodel import Field, SQLModel



class Debtor(SQLModel):
    name: str
    value: float


class Event(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, nullable=False)
    owner_name: str
    event_name: str
    debts: List[Debtor, ...] = Field(default_factory=list)


class Trip(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_name: str
    event_ids: List[uuid.UUID] = Field(default_factory=list)



class Link(SQLModel, table=True):
    value: str = Field(primary_key=True)
    id: uuid.UUID
    type: str

    @classmethod
    @field_validator("type")
    def validate_link_type(cls, v):
        if v not in ["event", "trip"]:
            raise ValueError("type must be 'event' or 'trip'")
        return v
