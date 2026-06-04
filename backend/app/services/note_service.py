from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.note import Note as NoteModel
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate


_NOTE_SORT_FIELDS = {
    "created_at": NoteModel.created_at,
    "updated_at": NoteModel.updated_at,
    "title": NoteModel.title
}


def create_note(
    db: Session,
    note: NoteCreate,
    current_user: User
):

    new_note = NoteModel(
        title=note.title,
        content=note.content,
        tags=note.tags,
        user_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


def get_all_notes(
    db: Session,
    current_user: User,
    skip: int,
    limit: int,
    sort_by: str,
    sort_dir: str,
    search: str | None
):

    if sort_by not in _NOTE_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )

    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_dir value"
        )

    sort_column = _NOTE_SORT_FIELDS[sort_by]

    order_by = sort_column.desc() if sort_dir == "desc" else sort_column.asc()

    query = db.query(NoteModel).filter(
        NoteModel.user_id == current_user.id,
        NoteModel.is_deleted.is_(False)
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                NoteModel.title.ilike(search_term),
                NoteModel.content.ilike(search_term),
                NoteModel.tags.ilike(search_term)
            )
        )

    return query.order_by(order_by).offset(skip).limit(limit).all()


def get_note_by_id(
    note_id: int,
    db: Session,
    current_user: User
):

    note = db.query(NoteModel).filter(
        NoteModel.id == note_id,
        NoteModel.user_id == current_user.id,
        NoteModel.is_deleted.is_(False)
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


def update_note(
    note_id: int,
    updated_note: NoteUpdate,
    db: Session,
    current_user: User
):

    note = db.query(NoteModel).filter(
        NoteModel.id == note_id,
        NoteModel.user_id == current_user.id,
        NoteModel.is_deleted.is_(False)
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content
    note.tags = updated_note.tags

    db.commit()
    db.refresh(note)

    return note


def delete_note(
    note_id: int,
    db: Session,
    current_user: User
):

    note = db.query(NoteModel).filter(
        NoteModel.id == note_id,
        NoteModel.user_id == current_user.id,
        NoteModel.is_deleted.is_(False)
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }
