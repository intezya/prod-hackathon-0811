from fastapi import APIRouter

from app.api.requests.debt import ForgiveDebtRequest, PayDebtRequest
from app.api.responses.debt import PayDebtResponse


router = APIRouter()


@router.patch("/update", response_model=PayDebtResponse)
async def repay(body: PayDebtRequest) -> PayDebtResponse: ...


# Headers: user_name (must be owner of an event)
@router.delete("/forgive", response_model=None)
async def forgive(body: ForgiveDebtRequest) -> None: ...
