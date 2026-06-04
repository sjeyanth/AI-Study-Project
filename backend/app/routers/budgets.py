from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetUpdate
from app.services import budget_service


router = APIRouter()


@router.get("/budgets", response_model=list[BudgetResponse])
def get_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return budget_service.get_all_budgets(
        db,
        current_user,
        skip,
        limit,
        month,
        year,
        sort_by,
        sort_dir
    )


@router.get("/budgets/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return budget_service.get_budget_by_id(
        budget_id,
        db,
        current_user
    )


@router.post("/budgets", response_model=BudgetResponse)
def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return budget_service.create_budget(
        db,
        budget,
        current_user
    )


@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    updated_budget: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return budget_service.update_budget(
        budget_id,
        updated_budget,
        db,
        current_user
    )


@router.delete("/budgets/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return budget_service.delete_budget(
        budget_id,
        db,
        current_user
    )
