from datetime import datetime

from pydantic import BaseModel, Field


class ReminderBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    tags: str | None = Field(default=None, max_length=500)
    due_date: datetime | None = None
    completed: bool = False


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
