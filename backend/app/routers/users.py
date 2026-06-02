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
from fastapi.security import OAuth2PasswordRequestForm


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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return user_service.login_user(
        db,
        form_data
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

@router.get("/my-tasks")
def my_tasks(
    current_user: User = Depends(get_current_user)
):

    return [
        {
            "title": task.title,
            "description": task.description
        }
        for task in current_user.tasks
    ]