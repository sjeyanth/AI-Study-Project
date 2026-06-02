from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.database.dependencies import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.services import user_service

from app.database.auth_dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return user_service.create_user(
        db,
        user
    )


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    return user_service.login_user(
        db,
        user
    )


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }