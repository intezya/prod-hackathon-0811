from sqlmodel import SQLModel


class CreateEvent(SQLModel):
    event_id: str
    link: str


class CreateTripEvent(SQLModel):
    event_id: str
