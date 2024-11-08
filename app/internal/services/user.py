import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, or_, select

from app.internal.config import settings
from app.internal.dependencies.base import SessionDep, TokenDep
from app.internal.security import ALGORITHM, get_password_hash, verify_password
from app.models import TokenPayload, User, UserCreate, UserRegister


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def check_if_user_exists(*, session: Session, data: UserRegister) -> bool:
    statement = select(User).where(
        or_(User.email == data.email, User.username == data.username)
    )
    user = session.exec(statement).first()
    return bool(user)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
