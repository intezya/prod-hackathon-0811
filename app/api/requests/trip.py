from sqlmodel import SQLModel


class CreateTripRequest(SQLModel):
    name: str
    allowed_names: str


class DeleteTripRequest(SQLModel):
    trip_id: str


class GetTripRequest(SQLModel):
    trip_id: str
