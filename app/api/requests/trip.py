from sqlmodel import SQLModel


class CreateTrip(SQLModel):
    name: str
    user_name: str
    user_names: str


class DeleteTrip(SQLModel):
    trip_id: str
    user_name: str
