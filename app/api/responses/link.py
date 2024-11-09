from typing import List

from pydantic import field_validator
from sqlmodel import SQLModel

from app.internal.db.models import EventView, TripView


class JoinByLinkResponse(SQLModel):
    context_type: str
    context_id: str
    allowed_names: List[str]
    data: TripView | EventView

    @classmethod
    @field_validator("context_type")
    def validate_context_type(cls, v):
        if v not in ["event", "trip"]:
            raise ValueError("context_type must be 'event' or 'trip'")
        return v
