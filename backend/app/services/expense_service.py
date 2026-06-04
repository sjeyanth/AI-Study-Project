from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.expense import Expense as ExpenseModel
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


_EXPENSE_SORT_FIELDS = {
    "created_at": ExpenseModel.created_at,
    "expense_date": ExpenseModel.expense_date,
    "amount": ExpenseModel.amount
}


def create_expense(
    db: Session,
    expense: ExpenseCreate,
    current_user: User
):

    new_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        expense_date=expense.expense_date,
        category=expense.category,
        notes=expense.notes,
        user_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def get_all_expenses(
    db: Session,
    current_user: User,
    skip: int,
    limit: int,
    category: str | None,
    start_date: datetime | None,
    end_date: datetime | None,
    sort_by: str,
    sort_dir: str,
    search: str | None
):

    if sort_by not in _EXPENSE_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )

    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_dir value"
        )

    sort_column = _EXPENSE_SORT_FIELDS[sort_by]

    order_by = sort_column.desc() if sort_dir == "desc" else sort_column.asc()

    query = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == current_user.id
    )

    if category:
        query = query.filter(ExpenseModel.category == category)

    if start_date:
        query = query.filter(ExpenseModel.expense_date >= start_date)

    if end_date:
        query = query.filter(ExpenseModel.expense_date <= end_date)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                ExpenseModel.title.ilike(search_term),
                ExpenseModel.category.ilike(search_term),
                ExpenseModel.notes.ilike(search_term)
            )
        )

    return query.order_by(order_by).offset(skip).limit(limit).all()


def get_expense_by_id(
    expense_id: int,
    db: Session,
    current_user: User
):

    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.user_id == current_user.id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


def update_expense(
    expense_id: int,
    updated_expense: ExpenseUpdate,
    db: Session,
    current_user: User
):

    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.user_id == current_user.id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.title = updated_expense.title
    expense.amount = updated_expense.amount
    expense.expense_date = updated_expense.expense_date
    expense.category = updated_expense.category
    expense.notes = updated_expense.notes

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(
    expense_id: int,
    db: Session,
    current_user: User
):

    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.user_id == current_user.id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }
