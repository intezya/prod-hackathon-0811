from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.internal.config import settings
from app.internal.db.core import get_db


SessionDep = Annotated[Session, Depends(get_db)]
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]
