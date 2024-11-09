from typing import List

from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import SQLModel
from starlette import status


class CreateTripRequest(SQLModel):
    name: str
    allowed_names: List[str]

    @classmethod
    @field_validator("allowed_names")
    def validate_debts(cls, value):
        if len(value) != len(set(value)):
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


class DeleteTripRequest(SQLModel):
    trip_id: str


class GetTripRequest(SQLModel):
    trip_id: str
