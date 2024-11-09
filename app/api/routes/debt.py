from fastapi import APIRouter

from app.api.requests.debt import PayDebtRequest
from app.api.responses.debt import PayDebtResponse


router = APIRouter()


@router.patch("/update", response_model=PayDebtResponse)
async def repay(body: PayDebtRequest) -> PayDebtResponse: ...
