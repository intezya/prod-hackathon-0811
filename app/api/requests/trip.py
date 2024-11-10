from typing import List

from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from starlette import status


class CreateTripRequest(SQLModel):
    name: str
    allowed_names: List[str] = Field(min_length=2)

    @field_validator("allowed_names")  # noqa
    @classmethod
    def validate_debts(cls, value):
        if len(value) != len(set(value)):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail={"message": "names must be unique"},
            )
        return value


class DeleteTripRequest(SQLModel):
    trip_id: str


class GetTripRequest(SQLModel):
    trip_id: str
