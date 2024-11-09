from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.requests.debt import ForgiveDebtRequest, PayDebtRequest
from app.api.responses.debt import PayDebtResponse
from app.internal.db.core import get_db
from app.internal.services.debt import pay_debt


router = APIRouter()


@router.patch("/update", response_model=PayDebtResponse)
async def repay(
    body: PayDebtRequest,
    session: AsyncSession = get_db(),
) -> PayDebtResponse:
    result = await pay_debt(session=session, req=body)
    return PayDebtResponse()


# Headers: user_name (must be owner of an event)
@router.delete("/forgive", response_model=None)
async def forgive(body: ForgiveDebtRequest) -> None: ...
