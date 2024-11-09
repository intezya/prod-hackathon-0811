from sqlmodel import SQLModel


class CreateTripRequest(SQLModel):
    name: str
    allowed_names: str


class DeleteTripRequest(SQLModel):
    trip_id: str
    owner_name: str


class GetTripRequest(SQLModel):
    trip_id: str
