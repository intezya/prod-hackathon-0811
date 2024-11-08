from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(min_length=5, max_length=32)
    password: str = Field(min_length=8, max_length=40)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdateMe(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, min_length=5, max_length=32)


class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
