import uuid
from typing import List, Optional

from pydantic import field_validator
from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlmodel import Field, SQLModel


class Debtor(SQLModel):
    name: str
    value: float


class Owner(SQLModel):
    name: str
    description: Optional[str]


class Event(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    owner_name: str
    owner_description: Optional[str]
    event_name: str
    debts: List[Debtor] = Field(
        default_factory=None,
        sa_column=Column(
            MutableList.as_mutable(
                ARRAY(MutableDict.as_mutable(JSON(none_as_null=True)))
            )
        ),
    )
    trip_id: uuid.UUID = Field(nullable=True, default=None)


class Trip(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_name: str
    event_ids: List[uuid.UUID] = Field(
        default_factory=None, sa_column=Column(MutableList.as_mutable(ARRAY(UUID)))
    )


class Link(SQLModel, table=True):
    value: str = Field(primary_key=True)
    id: uuid.UUID
    type: str
    allowed_user_names: List[str] = Field(
        default_factory=None, sa_column=Column(ARRAY(String))
    )

    @classmethod
    @field_validator("type")
    def validate_link_type(cls, v):
        if v not in ["event", "trip"]:
            raise ValueError("type must be 'event' or 'trip'")
        return v


class EventView(SQLModel):
    id: uuid.UUID
    event_name: str
    owner_name: str
    owner_description: Optional[str]
    debts: List[Debtor]


class TripView(SQLModel):
    id: uuid.UUID
    trip_name: str
    events: List[EventView]
