import hashlib
import uuid
from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.internal.db.models import Link


async def get_link_by_value(*, session: AsyncSession, value: str) -> Link | None:
    statement = select(Link).where(Link.value == value)
    result = await session.exec(statement)
    link = result.one_or_none()
    if link is not None:
        return link.model_copy()


async def create_link(
    *, session: AsyncSession, id: uuid.UUID, type: str, allowed_names: List[str]
) -> Link:
    value = hashlib.sha256(str(id).encode()).hexdigest()
    model = Link(
        value=value,
        id=id,
        type=type,
        allowed_user_names=allowed_names,
    )
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


async def get_link_by_id(*, session: AsyncSession, id: uuid.UUID) -> Link | None:
    statement = select(Link).where(Link.id == id)
    result = await session.exec(statement)
    link = result.one_or_none()
    if link is not None:
        return link.model_copy()


async def update_allowed_users_link_by_id(
    *,
    session: AsyncSession,
    id: uuid.UUID,
    new_allowed_user: str,
):
    statement = select(Link).where(Link.id == id)
    result = await session.exec(statement)
    link = result.one()
    link.allowed_user_names.append(new_allowed_user)
    await session.commit()
    await session.refresh(link)
    return
