from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.budget import Budget as BudgetModel
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate


_BUDGET_SORT_FIELDS = {
    "created_at": BudgetModel.created_at,
    "month": BudgetModel.month,
    "year": BudgetModel.year
}


def create_budget(
    db: Session,
    budget: BudgetCreate,
    current_user: User
):

    new_budget = BudgetModel(
        month=budget.month,
        year=budget.year,
        total_budget=budget.total_budget,
        currency=budget.currency,
        user_id=current_user.id
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget


def get_all_budgets(
    db: Session,
    current_user: User,
    skip: int,
    limit: int,
    month: int | None,
    year: int | None,
    sort_by: str,
    sort_dir: str
):

    if sort_by not in _BUDGET_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )

    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_dir value"
        )

    sort_column = _BUDGET_SORT_FIELDS[sort_by]

    order_by = sort_column.desc() if sort_dir == "desc" else sort_column.asc()

    query = db.query(BudgetModel).filter(
        BudgetModel.user_id == current_user.id
    )

    if month is not None:
        query = query.filter(BudgetModel.month == month)

    if year is not None:
        query = query.filter(BudgetModel.year == year)

    return query.order_by(order_by).offset(skip).limit(limit).all()


def get_budget_by_id(
    budget_id: int,
    db: Session,
    current_user: User
):

    budget = db.query(BudgetModel).filter(
        BudgetModel.id == budget_id,
        BudgetModel.user_id == current_user.id
    ).first()

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    return budget


def update_budget(
    budget_id: int,
    updated_budget: BudgetUpdate,
    db: Session,
    current_user: User
):

    budget = db.query(BudgetModel).filter(
        BudgetModel.id == budget_id,
        BudgetModel.user_id == current_user.id
    ).first()

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    budget.month = updated_budget.month
    budget.year = updated_budget.year
    budget.total_budget = updated_budget.total_budget
    budget.currency = updated_budget.currency

    db.commit()
    db.refresh(budget)

    return budget


def delete_budget(
    budget_id: int,
    db: Session,
    current_user: User
):

    budget = db.query(BudgetModel).filter(
        BudgetModel.id == budget_id,
        BudgetModel.user_id == current_user.id
    ).first()

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    db.delete(budget)
    db.commit()

    return {
        "message": "Budget deleted successfully"
    }
