from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.goal import Goal as GoalModel
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate


_GOAL_SORT_FIELDS = {
    "created_at": GoalModel.created_at,
    "updated_at": GoalModel.updated_at,
    "target_date": GoalModel.target_date,
    "title": GoalModel.title,
    "status": GoalModel.status,
    "progress": GoalModel.progress
}


def create_goal(
    db: Session,
    goal: GoalCreate,
    current_user: User
):

    new_goal = GoalModel(
        title=goal.title,
        description=goal.description,
        target_date=goal.target_date,
        status=goal.status,
        progress=goal.progress,
        user_id=current_user.id
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


def get_all_goals(
    db: Session,
    current_user: User,
    skip: int,
    limit: int,
    status: str | None,
    sort_by: str,
    sort_dir: str,
    search: str | None
):

    if sort_by not in _GOAL_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )

    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_dir value"
        )

    sort_column = _GOAL_SORT_FIELDS[sort_by]
    order_by = sort_column.desc() if sort_dir == "desc" else sort_column.asc()

    query = db.query(GoalModel).filter(
        GoalModel.user_id == current_user.id
    )

    if status:
        query = query.filter(GoalModel.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                GoalModel.title.ilike(search_term),
                GoalModel.description.ilike(search_term),
                GoalModel.status.ilike(search_term)
            )
        )

    return query.order_by(order_by).offset(skip).limit(limit).all()


def get_goal_by_id(
    goal_id: int,
    db: Session,
    current_user: User
):

    goal = db.query(GoalModel).filter(
        GoalModel.id == goal_id,
        GoalModel.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal


def update_goal(
    goal_id: int,
    updated_goal: GoalUpdate,
    db: Session,
    current_user: User
):

    goal = db.query(GoalModel).filter(
        GoalModel.id == goal_id,
        GoalModel.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    goal.title = updated_goal.title
    goal.description = updated_goal.description
    goal.target_date = updated_goal.target_date
    goal.status = updated_goal.status
    goal.progress = updated_goal.progress

    db.commit()
    db.refresh(goal)

    return goal


def delete_goal(
    goal_id: int,
    db: Session,
    current_user: User
):

    goal = db.query(GoalModel).filter(
        GoalModel.id == goal_id,
        GoalModel.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    db.delete(goal)
    db.commit()

    return {
        "message": "Goal deleted successfully"
    }