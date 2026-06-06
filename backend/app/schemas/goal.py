from datetime import datetime

from pydantic import BaseModel, Field


class GoalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    target_date: datetime
    status: str = Field(..., min_length=1, max_length=50)
    progress: int = Field(..., ge=0, le=100)


class GoalCreate(GoalBase):
    pass


class GoalUpdate(GoalBase):
    pass


class GoalResponse(GoalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True