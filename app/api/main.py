from app.api.routes import login, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])


@api_router.get("/health-check")
async def health_check() -> bool:
    return True
