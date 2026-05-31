from sqlalchemy.orm import Session
from app.models.task import Task as TaskModel
from app.schemas.task import Task
from fastapi import HTTPException


def create_task(
    db: Session,
    task: Task
):

    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task



def get_all_tasks(
    db: Session
):

    return db.query(
        TaskModel
    ).all()



def get_task_by_id(
    task_id: int,
    db: Session
):

    task = db.query(
        TaskModel
    ).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


def update_task(
    task_id: int,
    updated_task: Task,
    db: Session
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()

    db.refresh(task)

    return task


def delete_task(
    task_id: int,
    db: Session
):

    task = db.query(
        TaskModel
    ).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }