from datetime import datetime

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    tags: str | None = Field(default=None, max_length=500)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
