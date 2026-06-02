from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.task import Task
from app.schemas.task import TaskResponse
from app.database.dependencies import get_db
from app.services import task_service
from app.database.auth_dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.get_all_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    return task_service.get_task_by_id(
        task_id,
        db
    )


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: Task,
    db: Session = Depends(get_db)
):

    return task_service.create_task(
        db,
        task
    )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: Task,
    db: Session = Depends(get_db)
):

    return task_service.update_task(
        task_id,
        updated_task,
        db
    )


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    return task_service.delete_task(
        task_id,
        db
    )