from typing import List

from sqlmodel import SQLModel


class CreateEventResponse(SQLModel):
    event_id: str
    link: str


class CreateTripEventResponse(SQLModel):
    event_id: str


class AddDebtorResponse(SQLModel):
    link: str


class GetEventNamesResponse(SQLModel):
    names: List[str]
