from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reminder import Reminder as ReminderModel
from app.models.user import User
from app.schemas.reminder import ReminderCreate, ReminderUpdate


_REMINDER_SORT_FIELDS = {
    "created_at": ReminderModel.created_at,
    "updated_at": ReminderModel.updated_at,
    "due_date": ReminderModel.due_date,
    "title": ReminderModel.title
}


def create_reminder(
    db: Session,
    reminder: ReminderCreate,
    current_user: User
):

    new_reminder = ReminderModel(
        title=reminder.title,
        description=reminder.description,
        tags=reminder.tags,
        due_date=reminder.due_date,
        completed=reminder.completed,
        user_id=current_user.id
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    return new_reminder


def get_all_reminders(
    db: Session,
    current_user: User,
    skip: int,
    limit: int,
    sort_by: str,
    sort_dir: str,
    search: str | None
):

    if sort_by not in _REMINDER_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )

    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_dir value"
        )

    sort_column = _REMINDER_SORT_FIELDS[sort_by]

    order_by = sort_column.desc() if sort_dir == "desc" else sort_column.asc()

    query = db.query(ReminderModel).filter(
        ReminderModel.user_id == current_user.id,
        ReminderModel.is_deleted.is_(False)
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                ReminderModel.title.ilike(search_term),
                ReminderModel.description.ilike(search_term)
            )
        )

    return query.order_by(order_by).offset(skip).limit(limit).all()


def get_reminder_by_id(
    reminder_id: int,
    db: Session,
    current_user: User
):

    reminder = db.query(ReminderModel).filter(
        ReminderModel.id == reminder_id,
        ReminderModel.user_id == current_user.id,
        ReminderModel.is_deleted.is_(False)
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    return reminder


def update_reminder(
    reminder_id: int,
    updated_reminder: ReminderUpdate,
    db: Session,
    current_user: User
):

    reminder = db.query(ReminderModel).filter(
        ReminderModel.id == reminder_id,
        ReminderModel.user_id == current_user.id,
        ReminderModel.is_deleted.is_(False)
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    reminder.title = updated_reminder.title
    reminder.description = updated_reminder.description
    reminder.tags = updated_reminder.tags
    reminder.due_date = updated_reminder.due_date
    reminder.completed = updated_reminder.completed

    db.commit()
    db.refresh(reminder)

    return reminder


def delete_reminder(
    reminder_id: int,
    db: Session,
    current_user: User
):

    reminder = db.query(ReminderModel).filter(
        ReminderModel.id == reminder_id,
        ReminderModel.user_id == current_user.id,
        ReminderModel.is_deleted.is_(False)
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    db.delete(reminder)
    db.commit()

    return {
        "message": "Reminder deleted successfully"
    }
