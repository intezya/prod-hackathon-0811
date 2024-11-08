from datetime import timedelta
from typing import Annotated

from app.internal.config import settings
from app.internal.dependencies.base import SessionDep
from app.internal.security import create_access_token
from app.internal.services.user import authenticate_user
from app.models import Token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires)
    )
