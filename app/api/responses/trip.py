from sqlmodel import SQLModel


class CreateTrip(SQLModel):
    trip_id: str
    link: str


class DeleteTrip(SQLModel): ...