from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    class Config:
        from_attributes = True