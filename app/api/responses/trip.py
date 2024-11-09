from sqlmodel import SQLModel


class CreateTripResponse(SQLModel):
    trip_id: str
    link: str


class DeleteTripResponse(SQLModel): ...