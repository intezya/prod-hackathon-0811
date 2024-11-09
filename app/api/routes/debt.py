from fastapi import APIRouter


router = APIRouter()


@router.post("/new")
async def new_debt(body: ...) -> ...: ...


@router.patch("/update")
async def repay(body: ...) -> ...: ...
