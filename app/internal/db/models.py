import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, min_length=5, max_length=32)
    name: str | None = Field(default=None, max_length=255)



class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


    # Shared properties
