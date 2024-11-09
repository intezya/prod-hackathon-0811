from typing import List, Optional

from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from starlette import status

from app.internal.db.models import Debtor, Owner


class CreateEventRequest(SQLModel):
    event_name: str
    owner: Owner
    debts: List[Debtor] = Field(nullable=False, min_length=2)

    @field_validator("debts")  # noqa
    @classmethod
    def validate_debts(cls, value):
        print(123)
        if len(value) != len(set([item.name for item in value])):
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


class CreateTripEventRequest(SQLModel):
    event_name: str
    owner: Owner
    trip_id: str
    debts: List[Debtor] = Field(nullable=False, min_length=2)

    @field_validator("debts")  # noqa
    @classmethod
    def validate_debts(cls, value):
        if len(value) != len(set([item.name for item in value])):
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


class GetEventRequest(SQLModel):
    event_id: str


class AddDebtorRequest(SQLModel):
    # TODO: add unique debtor_name validation in repository/service layer
    event_id: str
    debtor_name: str
    debtor_value: float
    context_id: Optional[str]
