from datetime import datetime

from pydantic import BaseModel, Field


class BudgetBase(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)
    total_budget: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=1, max_length=10)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    pass


class BudgetResponse(BudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
