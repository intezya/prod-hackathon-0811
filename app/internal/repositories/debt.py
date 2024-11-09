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
    event = await session.execute(statement)
    new_value = -1

    for item in event.scalar().debts:
        if item.name == debtor.name:
            new_value = item.value - debtor.value
            item.value = new_value
            break

    await session.commit()
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
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if debtor.name in [item["name"] for item in event.debts]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    event.debts.append(debtor.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    link_context = await get_link_by_id(session=session, id=context_id)
    return link_context.value
