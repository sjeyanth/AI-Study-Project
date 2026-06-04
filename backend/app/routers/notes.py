from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.services import note_service


router = APIRouter()


@router.get("/notes", response_model=list[NoteResponse])
def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return note_service.get_all_notes(
        db,
        current_user,
        skip,
        limit,
        sort_by,
        sort_dir,
        search
    )


@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return note_service.get_note_by_id(
        note_id,
        db,
        current_user
    )


@router.post("/notes", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return note_service.create_note(
        db,
        note,
        current_user
    )


@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated_note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return note_service.update_note(
        note_id,
        updated_note,
        db,
        current_user
    )


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return note_service.delete_note(
        note_id,
        db,
        current_user
    )
