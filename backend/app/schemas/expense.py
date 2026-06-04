from datetime import datetime

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    expense_date: datetime
    category: str = Field(..., min_length=1, max_length=100)
    notes: str | None = Field(default=None, max_length=1000)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
