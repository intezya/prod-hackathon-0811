import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.requests.debt import PayDebtRequest
from app.internal.repositories.debt import repay_event_debtor_by_context_id


async def pay_debt(
    *,
    session: AsyncSession,
    req: PayDebtRequest,
):
    if req.trip_id is not None:  # TODO: check if trip equal ""
        context_id = req.trip_id
    else:
        context_id = req.event_id

    new_value = await repay_event_debtor_by_context_id(
        session=session,
        context_id=uuid.UUID(context_id),
        debtor=req.debtor,
    )
    return new_value
