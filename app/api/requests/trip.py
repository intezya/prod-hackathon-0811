from sqlmodel import SQLModel


class CreateTripRequest(SQLModel):
    name: str
    user_name: str
    user_names: str


class DeleteTripRequest(SQLModel):
    trip_id: str
    user_name: str
