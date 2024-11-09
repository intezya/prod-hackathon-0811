import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

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
) -> None:
    statement = select(Event).where(Event.id == event_id)
    event = await session.execute(statement)
    event.scalar().debts.append(debtor)

    link_context = get_link_by_id(session=session, id=context_id)
    await session.commit()
