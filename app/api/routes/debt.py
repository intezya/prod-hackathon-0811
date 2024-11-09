from fastapi import APIRouter

from app.api.requests.debt import DeleteDebtRequest, PayDebtRequest
from app.api.responses.debt import PayDebtResponse
from app.internal.db.core import SessionDep
from app.internal.services.debt import delete_debt, pay_debt


router = APIRouter()


@router.patch("", response_model=PayDebtResponse)
async def repay(
    body: PayDebtRequest,
    session: SessionDep,
) -> PayDebtResponse:
    result = await pay_debt(session=session, req=body)
    return result


# Headers: user_name (must be owner of an event)
@router.delete("", response_model=None)
async def delete(body: DeleteDebtRequest, session: SessionDep) -> None:
    await delete_debt(session=session, req=body)
