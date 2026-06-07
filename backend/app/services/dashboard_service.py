from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User


def get_dashboard_data(
    db: Session,
    current_user: User
):

    total_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id
    ).scalar()

    completed_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id,
        Task.completed == True
    ).scalar()

    pending_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id,
        Task.completed == False
    ).scalar()

    total_goals = db.query(
        func.count(Goal.id)
    ).filter(
        Goal.user_id == current_user.id
    ).scalar()

    completed_goals = db.query(
        func.count(Goal.id)
    ).filter(
        Goal.user_id == current_user.id,
        Goal.status == "completed"
    ).scalar()

    average_goal_progress = db.query(
        func.avg(Goal.progress)
    ).filter(
        Goal.user_id == current_user.id
    ).scalar()

    average_goal_progress = (
        average_goal_progress or 0
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "average_goal_progress": round(
            average_goal_progress,
            2
        )
    }