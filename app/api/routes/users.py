from typing import Any

from app.internal.dependencies.base import SessionDep
from app.internal.dependencies.user import CurrentUser
from app.internal.security import get_password_hash, verify_password
from app.internal.services.user import check_if_user_exists, create_user, get_user_by_email, get_user_by_username
from app.models import (
    Message,
    UserCreate,
    UserPublic,
    UserRegister,
    UserUpdateMe,
    UserUpdatePassword,
)
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/register", response_model=UserPublic)
def register_user(session: SessionDep, data: UserRegister) -> Any:
    user_exists = check_if_user_exists(session=session, data=data)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists",
        )
    user_create = UserCreate.model_validate(data)
    new_user = create_user(session=session, user_create=user_create)
    return new_user


@router.get("/me", response_model=UserPublic)
def get_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    session.delete(current_user)
    session.commit()
    return Message(message="User deleted successfully")


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    if user_in.username:
        existing_user = get_user_by_username(session=session, username=user_in.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this username already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UserUpdatePassword, current_user: CurrentUser
) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")
