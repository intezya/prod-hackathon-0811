import uuid
from collections import defaultdict
from typing import Dict, List

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.requests.debt import DeleteDebtRequest, PayDebtRequest
from app.api.responses.debt import PayDebtResponse
from app.internal.db.models import Debtor, EventView
from app.internal.repositories.debt import (
    delete_user_debt_from_event,
    repay_event_debtor_by_context_id,
)
from app.internal.services.events import get_event_view
from app.internal.websocket_messages.debt import debt_paid_out_notify


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
    await debt_paid_out_notify(
        data=await get_event_view(session=session, event_id=req.event_id),
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


async def deduct_debt(
    session: AsyncSession,
    events: List[EventView],
) -> List[Debtor]:
    debt_matrix = defaultdict(lambda: defaultdict(float))

    for event in events:
        owner = event.owner_name
        for debt in event.debts:
            debt_matrix[debt.name][owner] += debt.value

    all_people = set(
        person
        for event in events
        for person in [event.owner_name] + [debt.name for debt in event.debts]
    )

    for person1 in all_people:
        for person2 in all_people:
            if person1 != person2:
                debt1 = debt_matrix[person1][person2]
                debt2 = debt_matrix[person2][person1]

                if debt1 > debt2:
                    debt_matrix[person1][person2] = debt1 - debt2
                    debt_matrix[person2][person1] = 0
                else:
                    debt_matrix[person2][person1] = debt2 - debt1
                    debt_matrix[person1][person2] = 0

    result: Dict[str, List[Debtor]] = {}
    for person1 in all_people:
        debtors = []
        for person2, amount in debt_matrix[person1].items():
            if amount > 0:
                debtors.append(Debtor(name=person2, value=amount))
        if debtors:
            result[person1] = debtors

    return result
