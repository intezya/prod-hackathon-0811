from fastapi import FastAPI

from app.api.main import api_router


app = FastAPI(
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # redoc_url=None,
)

app.include_router(api_router, prefix="/api")
