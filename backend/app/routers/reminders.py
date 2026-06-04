from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.reminder import ReminderCreate, ReminderResponse, ReminderUpdate
from app.services import reminder_service


router = APIRouter()


@router.get("/reminders", response_model=list[ReminderResponse])
def get_reminders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return reminder_service.get_all_reminders(
        db,
        current_user,
        skip,
        limit,
        sort_by,
        sort_dir,
        search
    )


@router.get("/reminders/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return reminder_service.get_reminder_by_id(
        reminder_id,
        db,
        current_user
    )


@router.post("/reminders", response_model=ReminderResponse)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return reminder_service.create_reminder(
        db,
        reminder,
        current_user
    )


@router.put("/reminders/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    updated_reminder: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return reminder_service.update_reminder(
        reminder_id,
        updated_reminder,
        db,
        current_user
    )


@router.delete("/reminders/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return reminder_service.delete_reminder(
        reminder_id,
        db,
        current_user
    )
