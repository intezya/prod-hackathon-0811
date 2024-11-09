import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.requests.debt import DeleteDebtRequest, PayDebtRequest
from app.api.responses.debt import PayDebtResponse
from app.internal.db.models import Debtor
from app.internal.repositories.debt import (
    delete_user_debt_from_event,
    repay_event_debtor_by_context_id,
)


async def pay_debt(
    *,
    session: AsyncSession,
    req: PayDebtRequest,
) -> PayDebtResponse:
    new_value = await repay_event_debtor_by_context_id(
        session=session,
        context_id=uuid.UUID(req.event_id),
        debtor=Debtor(name=req.debtor_name, value=req.pay_value),
    )
    return PayDebtResponse(new_value=new_value)


async def delete_debt(
    *,
    session: AsyncSession,
    req: DeleteDebtRequest,
) -> None:
    await delete_user_debt_from_event(
        session=session,
        event_id=uuid.UUID(req.event_id),
        debtor_name=req.debtor_name,
    )
