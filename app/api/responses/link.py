from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import SQLModel
from starlette import status

from app.internal.db.models import EventView, TripView


class JoinByLinkResponse(SQLModel):
    context_type: str
    context_id: str
    data: TripView | EventView

    @classmethod
    @field_validator("context_type")
    def validate_context_type(cls, v):
        if v not in ["event", "trip"]:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {"message": "context_type must be 'event' or 'trip'"},
            )
        return v
