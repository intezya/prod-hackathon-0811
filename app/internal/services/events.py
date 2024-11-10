import uuid

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.api.requests.debt import DeleteDebtRequest
from app.api.requests.event import (
    AddDebtorRequest,
    CreateEventRequest,
    GetEventNamesRequest,
)
from app.api.responses.event import (
    AddDebtorResponse,
    CreateEventResponse,
    GetEventNamesResponse,
)
from app.internal.config import settings
from app.internal.db.models import Debtor, EventView
from app.internal.repositories.debt import add_debtor_to_event_by_context_id
from app.internal.repositories.events import (
    create_event,
    delete_event_by_id,
    get_event_by_id,
    get_event_names_by_event_id,
)
from app.internal.repositories.links import (
    create_link,
    get_link_by_value,
    update_allowed_users_link_by_id,
)
from app.internal.websocket_messages.event import new_debtor_in_event_added_notify


async def get_event_view(
    *,
    session: AsyncSession,
    event_id: str,
) -> EventView:
    event_id = str(uuid.UUID(event_id))
    event = await get_event_by_id(session=session, id=uuid.UUID(event_id))
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "event not found"},
        )
    event_view = EventView(
        id=event.id,
        event_name=event.event_name,
        debts=event.debts,
        owner_name=event.owner_name,
        owner_description=event.owner_description,
    )
    return event_view


async def create_event_view(
    *,
    session: AsyncSession,
    create_event_req: CreateEventRequest,
) -> CreateEventResponse:
    # create event -> link by id
    event = await create_event(session=session, create_event_req=create_event_req)
    link = await create_link(
        session=session,
        id=event.id,
        type="event",
        allowed_names=[i.name for i in create_event_req.debts],
    )
    event_resp = CreateEventResponse(
        event_id=str(event.id),
        link=f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}/link/{link.value}",  # noqa
    )
    return event_resp


async def add_debtor_to_event(
    session: AsyncSession,
    req: AddDebtorRequest,
) -> AddDebtorResponse:
    link_value = await add_debtor_to_event_by_context_id(
        session=session,
        event_id=uuid.UUID(req.event_id),
        context_id=uuid.UUID(req.context_id),
        debtor=Debtor(name=req.debtor_name, value=req.debtor_value),
    )

    await update_allowed_users_link_by_id(
        session=session,
        id=uuid.UUID(req.context_id),
        new_allowed_user=req.debtor_name,
    )

    await new_debtor_in_event_added_notify(
        data=await get_event_view(session=session, event_id=req.event_id),
        context_id=req.event_id,
    )
    return AddDebtorResponse(
        link=f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}/link/{link_value}"
    )


async def delete_event(session: AsyncSession, req: DeleteDebtRequest) -> None:
    event_id = uuid.UUID(req.event_id)
    await delete_event_by_id(session=session, id=event_id)


async def get_event_names_by_link(
    session: AsyncSession, req: GetEventNamesRequest
) -> GetEventNamesResponse:
    link_value = req.link.split("/")[-1]
    link = await get_link_by_value(session=session, value=link_value)

    if link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    result = await get_event_names_by_event_id(
        session=session,
        event_id=link.id,
    )
    return result
