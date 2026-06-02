from sqlalchemy.orm import Session
from app.models.task import Task as TaskModel
from app.schemas.task import Task
from fastapi import HTTPException
from app.models.user import User


def create_task(
    db: Session,
    task: Task,
    current_user: User

):

    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task



def get_all_tasks(
    db: Session,
    current_user: User
):

    return db.query(
        TaskModel
    ).filter(
    TaskModel.user_id == current_user.id
).all()



def get_task_by_id(
    task_id: int,
    db: Session,
    current_user: User 
):

    task = db.query(
    TaskModel
).filter(
    TaskModel.id == task_id,
    TaskModel.user_id == current_user.id
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
    db: Session,
    current_user: User
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id        
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
    db: Session,
    current_user: User
):

    task = db.query(
        TaskModel
    ).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id
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