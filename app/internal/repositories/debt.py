import uuid

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.internal.db.models import Debtor, Event
from app.internal.repositories.links import get_link_by_id


async def repay_event_debtor_by_context_id(
    *,
    session: AsyncSession,
    context_id: uuid.UUID,
    debtor: Debtor,
) -> int:
    statement = select(Event).where(Event.id == context_id)
    result = await session.exec(statement)
    event = result.one()

    if event is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    new_debts = []

    for item in event.debts:
        if item["name"] == debtor.name:
            new_value = item["value"] - debtor.value
            if new_value < 0:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)
            if new_value > 0:
                new_debts.append({"name": item["name"], "value": new_value})
            else:
                pass

        else:
            if item["value"] > 0:
                new_debts.append(item)
    event.debts = new_debts
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return new_value


async def add_debtor_to_event_by_context_id(
    *,
    session: AsyncSession,
    event_id: uuid.UUID,
    debtor: Debtor,
    context_id: uuid.UUID,
) -> str:
    statement = select(Event).where(Event.id == event_id)
    result = await session.exec(statement)
    event = result.one()
    if not event:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": "event not found"},
        )
    if debtor.name in [item["name"] for item in event.debts]:  # type: ignore
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "debtor already exists"},
        )

    event.debts.append(debtor.model_dump())  # type: ignore
    session.add(event)
    await session.commit()
    await session.refresh(event)
    link_context = await get_link_by_id(session=session, id=context_id)
    return link_context.model_copy().value


async def delete_user_debt_from_event(
    *,
    session: AsyncSession,
    event_id: uuid.UUID,
    debtor_name: str,
):
    statement = select(Event).where(Event.id == event_id)
    result = await session.exec(statement)
    event = result.one()
    if not event:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": "event not found"},
        )
    new_debts = []
    for item in event.debts:
        if item["name"] != debtor_name:
            new_debts.append(item)
    event.debts = new_debts
    session.add(event)
    await session.commit()
    await session.refresh(event)
