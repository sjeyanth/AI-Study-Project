from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services import expense_service


router = APIRouter()


@router.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return expense_service.get_all_expenses(
        db,
        current_user,
        skip,
        limit,
        category,
        start_date,
        end_date,
        sort_by,
        sort_dir,
        search
    )


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return expense_service.get_expense_by_id(
        expense_id,
        db,
        current_user
    )


@router.post("/expenses", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return expense_service.create_expense(
        db,
        expense,
        current_user
    )


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    updated_expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return expense_service.update_expense(
        expense_id,
        updated_expense,
        db,
        current_user
    )


@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return expense_service.delete_expense(
        expense_id,
        db,
        current_user
    )
