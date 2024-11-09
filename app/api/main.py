from fastapi import APIRouter

from app.api.routes import debt, event, link, trip, websocket


api_router = APIRouter()
api_router.include_router(debt.router, prefix="/debt", tags=["debts"])
api_router.include_router(event.router, prefix="/event", tags=["events"])
api_router.include_router(trip.router, prefix="/trip", tags=["trip"])
api_router.include_router(websocket.router, prefix="/websocket", tags=["websocket"])
api_router.include_router(link.router, prefix="/link", tags=["link"])


@api_router.get("/health-check")
async def health_check() -> bool:
    return True
