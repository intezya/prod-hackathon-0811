from fastapi import APIRouter


router = APIRouter()


@router.post("/new")
async def new_trip(body: ...) -> ...: ...


@router.get("")
async def get_trip(body: ...) -> ...: ...


@router.delete("")
async def delete_trip(body: ...) -> ...: ...