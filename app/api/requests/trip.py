from sqlmodel import SQLModel


class CreateTrip(SQLModel):
    name: str
    user_names: str
